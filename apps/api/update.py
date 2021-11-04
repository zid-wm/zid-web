import ast
import os
import pytz

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.utils import timezone

from .models import Controller
from apps.user.models import User
from util.vatsim.data import vatsim_controllers


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(pull_controllers, 'interval', minutes=1)
    scheduler.start()


def pull_controllers():
    atc_clients = vatsim_controllers()
    update_existing_controllers(atc_clients)
    add_new_controllers(atc_clients)


def update_existing_controllers(atc_clients):
    for controller in Controller.objects.all():
        controller_data = next((entry for entry in atc_clients if entry['callsign'] == controller.callsign), None)
        if controller_data:
            controller.last_update = timezone.now()
            controller.frequency = controller_data['frequency']
            controller.save()
        else:
            controller.convert_to_session()
            controller.delete()


def add_new_controllers(atc_clients):
    airports = ast.literal_eval(os.getenv('CONTROLLED_FIELDS'))

    for controller in atc_clients:
        user = User.objects.filter(cid=controller['cid'])
        if user.exists() \
                and controller['facility'] != 0 \
                and controller['callsign'].split('_')[0] in airports:
            if not Controller.objects.filter(callsign=controller['callsign']).exists():
                Controller(
                    user=user.first(),
                    callsign=controller['callsign'],
                    frequency=controller['frequency'],
                    online_since=pytz.utc.localize(
                        datetime.strptime(controller['logon_time'][:-2], '%Y-%m-%dT%H:%M:%S.%f')),
                    last_update=timezone.now()
                ).save()
