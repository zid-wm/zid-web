import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zid_web.settings')
django.setup()

from apps.administration.models import (
    ActionLog,
    MAVP
)


def test_action_log_str():
    action_log = ActionLog(
        action='Test Action'
    )
    assert '| Test Action' in str(action_log)


def test_mavp_str():
    mavp = MAVP(
        facility_short='ZAB',
        facility_long='Test Facility'
    )
    assert str(mavp) == 'Test Facility (ZAB)'
