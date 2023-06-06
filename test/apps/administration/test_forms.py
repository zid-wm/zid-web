import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zid_web.settings')
django.setup()

# pylint: disable=wrong-import-position,wrong-import-order
from apps.administration.forms import (
    SendEmailForm,
    StaffCommentForm
)
from test.helpers import test_data_factory


def test_send_email_form():
    request = test_data_factory.get_request('/email/send/')
    send_email_form = SendEmailForm(request)
    assert len(send_email_form.fields['ratings'].choices) == 10
    assert send_email_form.fields['sender_name'].initial == 'FirstName LastName'
    assert send_email_form.fields['reply_email'].initial == 'first.last@mail.com'


def test_staff_comment_form():
    staff_comment_form = StaffCommentForm('FirstName LastName')
    assert staff_comment_form.fields['subject'].initial == 'FirstName LastName'
