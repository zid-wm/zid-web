import os
import requests

from django.core import mail
from django.template.loader import render_to_string

from apps.user.models import User
from zid_web.decorators import run_async


@run_async
def send_visitor_approval_email(cid, approver_name):
    user = User.objects.get(
        cid=cid
    )

    html_msg = render_to_string('email/EMAIL_visitor_app_approve.html', {
        'user': user,
        'approver_name': approver_name
    })

    mail_data = [mail.EmailMultiAlternatives(
        'Visiting Application Accepted',
        html_msg,
        to=[user.email]
    )]

    mail_data[0].attach_alternative(html_msg, 'text/html')

    with mail.get_connection() as conn:
        conn.send_messages(mail_data)


@run_async
def send_visitor_denial_email(cid):
    visitor_email = requests.get(
        f'https://api.vatusa.net/v2/user/{cid}',
        params={
            'apikey': os.getenv('API_KEY')
        }
    ).json()['email']

    html_msg = render_to_string('email/EMAIL_visitor_app_deny.html')

    mail_data = [mail.EmailMultiAlternatives(
        'Visiting Application Denied',
        html_msg,
        to=[visitor_email]
    )]

    mail_data[0].attach_alternative(html_msg, 'text/html')

    with mail.get_connection() as conn:
        conn.send_messages(mail_data)


@run_async
def send_broadcast_email(request, subject, message, reply_email, email_list):
    html_msg = render_to_string(
        'email/EMAIL_std.html',
        {
            'body': message,
            'sender': request.user_obj.full_name
        }
    )
    mail_data = [mail.EmailMultiAlternatives(
        subject,
        message,
        to=[item['email']],
        reply_to=[reply_email]
    ) for item in email_list]

    for item in mail_data:
        item.attach_alternative(html_msg, 'text/html')

    with mail.get_connection() as conn:
        conn.send_messages(mail_data)


@run_async
def send_event_request_email(request):
    html_msg = render_to_string(
        'email/EMAIL_event_request.html',
        {
            'requester_name': request.POST['name'],
            'requester_email': request.POST['email'],
            'requester_org': request.POST['organization'],
            'description': request.POST['description']
        }
    )
    mail_data = [mail.EmailMultiAlternatives(
        'New Event Request',
        html_msg,
        to=['ec@zidartcc.org'],
        cc=['atm@zidartcc.org', 'datm@zidartcc.org']
    )]

    mail_data[0].attach_alternative(html_msg, 'text/html')
    with mail.get_connection() as conn:
        conn.send_messages(mail_data)
