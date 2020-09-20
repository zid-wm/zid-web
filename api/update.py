import ast
import os
import requests
import pytz

from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime

from django.utils import timezone

from .models import Controller, ControllerSession
from user.models import User


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(pull_controllers, 'interval', minutes=1)
    scheduler.start()


def pull_controllers():
    airports = ast.literal_eval(os.getenv('CONTROLLED_FIELDS'))
    data_file = requests.get('http://us.data.vatsim.net/vatsim-data.txt').text
    data = [line.split(':') for line in data_file.split('\n')]
    atc_clients = {client[0]: client for client in data
                   if len(client) == 42 and client[3] == 'ATC'}

    for controller in Controller.objects.all():
        if controller.callsign in atc_clients:
            controller.last_update = timezone.now()
            controller.save()
        else:
            ControllerSession(
                user=controller.user,
                callsign=controller.callsign,
                start=controller.online_since,
                duration=controller.last_update - controller.online_since
            ).save()
            controller.delete()

    for callsign, controller in atc_clients.items():
        if controller[1] and User.objects.filter(cid=controller[1]).exists():
            split = callsign.split('_')
            if split[0] in airports:
                if split[-1] in ['FD', 'DEL', 'GND', 'TWR', 'DEP', 'APP', 'CTR', 'FSS']:
                    if not Controller.objects.filter(callsign=callsign).exists():
                        Controller(
                            user=User.objects.get(cid=int(controller[1])),
                            callsign=callsign,
                            frequency=controller[4],
                            online_since=pytz.utc.localize(
                                datetime.strptime(controller[36], '%Y%m%d%H%M%S')),
                            last_update=timezone.now()
                        ).save()
