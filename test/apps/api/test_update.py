import os
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zid_web.settings')
django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from test.helpers import test_data_factory
from test.helpers.conftest import VATSIM_DATA, VATSIM_STATUS
from apps.api import update
from apps.api.models import Controller, ControllerSession


def create_user():
    user = test_data_factory.controller()
    user.save()
    return user


def test_start(mocker):
    add_job = mocker.patch.object(BackgroundScheduler, 'add_job')
    start = mocker.patch.object(BackgroundScheduler, 'start')
    update.start()

    assert add_job.call_count == 1
    assert start.call_count == 1


@pytest.mark.django_db
def test_pull_controllers(requests_mock):
    requests_mock.get('https://status.vatsim.net/status.json', json=VATSIM_STATUS)
    requests_mock.get('https://data.vatsim.net/v3/vatsim-data.json', json=VATSIM_DATA)
    create_user()

    update.pull_controllers()

    assert Controller.objects.filter(callsign='SDF_TWR').exists()


@pytest.mark.django_db
def test_pull_controllers_remove(requests_mock):
    user = create_user()
    ControllerSession(
        user=user,
        callsign='SDF_TWR',
        frequency=124.200,
        online_since=datetime.strptime()
    )
    new_vatsim_data = VATSIM_DATA.copy()
    new_vatsim_data['controllers'] = []
    requests_mock.get('https://data.vatsim.net/v3/vatsim-data.json', json=new_vatsim_data)
    update.pull_controllers()
    assert not Controller.objects.filter(callsign='SDF_TWR').exists()
    assert ControllerSession.objects.filter(callsign='SDF_TWR').exists()
