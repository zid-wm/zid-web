import os
import django
import pytest

from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zid_web.settings')
django.setup()

from apps.event.models import *
from test.helpers import test_data_factory


def create_event():
    event = Event(
        name='Event1',
        banner=None,
        start=datetime.strptime('2023-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        end=datetime.strptime('2023-01-01T01:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        host='ZID',
        description=None,
        hidden=False
    )
    event.save()
    return event


@pytest.mark.django_db
def test_event():
    event = create_event()

    assert event.duration == timedelta(minutes=60)
    assert str(event) == 'Event1'


@pytest.mark.django_db
def test_event_position_cab():
    user = test_data_factory.controller()
    user.save()
    event_position = EventPosition(
        event=create_event(),
        user=user,
        callsign='SDF_TWR'
    )

    assert event_position.category == 'cab'


@pytest.mark.django_db
def test_event_position_tracon():
    user = test_data_factory.controller()
    user.save()
    event_position = EventPosition(
        event=create_event(),
        user=user,
        callsign='SDF_APP'
    )

    assert event_position.category == 'tracon'


@pytest.mark.django_db
def test_event_position_center():
    user = test_data_factory.controller()
    user.save()
    event_position = EventPosition(
        event=create_event(),
        user=user,
        callsign='IND_CTR'
    )

    assert event_position.category == 'center'


@pytest.mark.django_db
def test_event_signup():
    user = test_data_factory.controller()
    user.save()

    event_position = EventPosition(
        event=create_event(),
        user=None,
        callsign='SDF_TWR'
    )

    event_signup = EventSignup(
        position=event_position,
        user=user
    )

    event_signup.assign()
    assert event_position.user.cid == user.cid


def test_position_preset():
    position_preset = PositionPreset(
        name='SDF Preset',
        positions_json='["SDF_TWR", "SDF_APP", "IND_CTR"]'
    )

    assert len(position_preset.positions) == 3
    assert 'SDF_TWR' in position_preset.positions
    assert str(position_preset) == 'SDF Preset'


def test_position_preset_set():
    position_preset = PositionPreset(
        name='IND Preset'
    )
    position_preset.set_positions(['IND_TWR', 'IND_APP', 'IND_CTR'])

    assert len(position_preset.positions) == 3
    assert 'IND_TWR' in position_preset.positions


@pytest.mark.django_db
def test_position_preset_add():
    event = create_event()
    position_preset = PositionPreset(
        name='SDF Preset',
        positions_json='["SDF_TWR", "SDF_APP", "IND_CTR"]'
    )

    position_preset.add_to_event(event)
    assert EventPosition.objects.filter().count() == 3

    twr = EventPosition.objects.get(callsign='SDF_TWR')
    assert twr.user is None
    assert twr.event.name == 'Event1'
