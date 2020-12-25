from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.user.models import User


def send_visitor_approval_email(cid, approver_name):
    user = User.objects.get(
        cid=cid
    )

    send_mail(
        'Visiting Application Accepted',
        render_to_string('EMAIL_visitor_app_approve.html', {
            'user': user,
            'approver_name': approver_name
        }),
        'no-reply@zidartcc.org',
        [user.email]
    )
