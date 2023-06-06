import os
import django
import pytest

from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zid_web.settings')
django.setup()

from apps.api.models import (
    Controller,
    ControllerSession
)
from test.helpers import test_data_factory


def test_controller():
    controller = Controller(
        user=test_data_factory.controller(),
        callsign='IND_CTR',
        frequency=119.550,
        online_since=datetime.strptime('2023-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        last_update=datetime.strptime('2023-01-01T01:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    )
    assert controller.duration == timedelta(minutes=60)
    assert str(controller) == 'FirstName LastName on IND_CTR'


def test_controller_session():
    controller_session = ControllerSession(
        user=test_data_factory.controller(),
        callsign='IND_CTR',
        start=datetime.strptime('2023-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        duration=timedelta(minutes=60)
    )
    assert controller_session.end == datetime.strptime('2023-01-01T01:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    assert str(controller_session) == '2023-01-01 00:00:00 | FirstName LastName on IND_CTR'


@pytest.mark.django_db
def test_convert_to_session():
    user = test_data_factory.controller()
    user.save()

    controller = Controller(
        user=test_data_factory.controller(),
        callsign='IND_CTR',
        frequency=119.550,
        online_since=datetime.strptime('2023-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        last_update=datetime.strptime('2023-01-01T01:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    )

    controller.convert_to_session()
    assert ControllerSession.objects.filter(user=user).exists()

    controller_session = ControllerSession.objects.get(user=user)
    end_time = datetime.strptime('2023-01-01T01:00:00 UTC', '%Y-%m-%dT%H:%M:%S %Z')
    assert controller_session.end.strftime('%Y-%m-%dT%H:%M:%SZ') == '2023-01-01T01:00:00Z'
    assert str(controller_session) == '2023-01-01 00:00:00+00:00 | FirstName LastName on IND_CTR'
