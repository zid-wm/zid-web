import boto3
import calendar
import os
import requests

from datetime import date
from django.core import mail
from django.template.loader import render_to_string

from apps.user.models import User
from zid_web.decorators import run_async


def send_email(subject, message, html_message, to_email, *args, **kwargs):
    client = boto3.client('ses', region_name='us-east-1')

    response = client.send_email(
        Source=kwargs.get('from_email', default='noreply@zidartcc.org'),
        Destination={
            'ToAddresses': to_email
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': message,
                    'Charset': 'UTF-8'
                },
                'Html': {
                    'Data': html_message,
                    'Charset': 'UTF-8'
                }
            }
        }
    )


@run_async
def send_visitor_approval_email(cid, approver_name):
    user = User.objects.get(
        cid=cid
    )

    html_msg = render_to_string('email_html/EMAIL_visitor_app_approve.html', {
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

    html_msg = render_to_string('email_html/EMAIL_visitor_app_deny.html')

    mail_data = [mail.EmailMultiAlternatives(
        'Visiting Application Denied',
        html_msg,
        to=[visitor_email]
    )]

    mail_data[0].attach_alternative(html_msg, 'text/html')

    with mail.get_connection() as conn:
        conn.send_messages(mail_data)


def send_visit_request_notification_email(request):
    html_msg = render_to_string(
        'email_html/EMAIL_visit_request_notification.html',
        {
            'requester_name': request.POST['name'],
            'description': request.POST['description']
        }
    )
    txt_msg = render_to_string(
        'email_txt/EMAIL_visit_request_notification.txt',
        {
            'requester_name': request.POST['name'],
            'description': request.POST['description']
        }
    )

    for email in ['atm@zidartcc.org', 'datm@zidartcc.org', 'wm@zidartcc.org']:
        send_email('New Visit Request', txt_msg, html_msg, email)


@run_async
def send_broadcast_email(request, subject, message, reply_email, email_list):
    html_msg = render_to_string(
        'email_html/EMAIL_std.html',
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
        'email_html/EMAIL_event_request.html',
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


@run_async
def send_inactivity_warning_email(email_list):
    html_msg = render_to_string(
        'email_html/EMAIL_inactivity.html',
        {
            'month': calendar.month_name[date.today().month]
        }
    )
    mail_data = [mail.EmailMultiAlternatives(
        'Controller Inactivity Warning',
        html_msg,
        to=[email['email']]
    ) for email in email_list]

    for item in mail_data:
        item.attach_alternative(html_msg, 'text/html')
    with mail.get_connection() as conn:
        conn.send_messages(mail_data)
