import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zid_web.settings')
django.setup()

# pylint: disable=wrong-import-position,wrong-import-order
from apps.event.forms import (
    NewEventForm,
    EditEventForm,
    AddPositionForm
)


def test_new_event_form():
    new_event_form = NewEventForm()
    assert len(new_event_form.fields) == 6


def test_edit_event_form():
    edit_event_form = EditEventForm()
    assert len(edit_event_form.fields) == 6


def test_add_position_form():
    add_position_form = AddPositionForm()
    assert len(add_position_form.fields) == 1
