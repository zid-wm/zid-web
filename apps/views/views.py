import logging
import requests
import os

from datetime import date
from django.shortcuts import render
from django.db.models import Sum, Q
from django.http import HttpResponse
from json import JSONDecodeError

from apps.api.models import Controller, ControllerSession
from apps.user.models import User
from apps.news.models import NewsArticle
from util.alert import MESSAGES


LOGGER = logging.getLogger(__name__)


def get_leaderboard(month, year):
    return ControllerSession.objects \
        .filter(
            start__year=year,
            start__month=month
        ) \
        .values('user', 'user__first_name', 'user__last_name') \
        .annotate(duration=Sum('duration')) \
        .order_by('-duration')[0:5]


def get_leaderboard_by_position(month, year, pos):
    return ControllerSession.objects \
        .filter(
            start__year=year,
            start__month=month,
            callsign__endswith=pos
        ) \
        .values('user', 'user__first_name', 'user__last_name') \
        .annotate(duration=Sum('duration')) \
        .order_by('-duration')[0:5]


def view_home(request):
    online_controllers_count = Controller.objects.count()
    total_home_controllers = User.objects.filter(main_role='HC', status=0).count()

    now = date.today()
    month = now.month
    year = now.year
    month_control_time = ControllerSession.objects.filter(
        start__year=year,
        start__month=month
    ).aggregate(
        Sum('duration'))['duration__sum']

    if request.GET.get('m', False):
        message_no = int(request.GET.get('m', 0))
        if message_no in MESSAGES:
            message = MESSAGES[message_no]
        else:
            message = MESSAGES[0]
    else:
        message = None

    try:
        # The timeout is set to slightly longer than a standard TCP packet retransmission window.
        pilots = requests.get('https://api.denartcc.org/live/ZID', timeout=3.05).json()
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        pilots = []
    except JSONDecodeError:
        # TODO: Add logging here
        pilots = []

    online_controllers = Controller.objects.all()

    now = date.today()
    total_this_month = get_leaderboard(now.month, now.year)

    last_month = now.month - 1 if now.month > 1 else 12
    last_month_yr = now.year if now.month > 1 else now.year - 1
    total_last_month = get_leaderboard(last_month, last_month_yr)

    ctr_this_month = get_leaderboard_by_position(now.month, now.year, 'CTR')
    app_this_month = get_leaderboard_by_position(now.month, now.year, 'APP')
    twr_this_month = get_leaderboard_by_position(now.month, now.year, 'TWR')

    gnd_this_month = ControllerSession.objects \
        .filter(
            Q(start__year=now.year) &
            Q(start__month=now.month) &
            (Q(callsign__endswith='GND') | Q(callsign__endswith='DEL'))
        ) \
        .values('user', 'user__first_name', 'user__last_name') \
        .annotate(duration=Sum('duration')) \
        .order_by('-duration')[0:5]

    dev_env = os.getenv('ENVIRONMENT').lower() != 'prod'

    latest_news = NewsArticle.objects.all().values(
        'title', 'date_posted', 'id'
    ).order_by('-date_posted')[0:3]

    return render(request, 'home.html', {
        'page_title': 'Home',
        'online_controllers_count': online_controllers_count,
        'total_home_controllers': total_home_controllers,
        'month_control_time': month_control_time,
        'pilots': pilots,
        'pilots_in_airspace': len(pilots),
        'online_controllers': online_controllers,
        'total_this_month': total_this_month,
        'total_last_month': total_last_month,
        'ctr_this_month': ctr_this_month,
        'app_this_month': app_this_month,
        'twr_this_month': twr_this_month,
        'gnd_this_month': gnd_this_month,
        'dev_env': dev_env,
        'message': message,
        'latest_news': latest_news
    })


def view_privacy_policy(request):
    return render(request, 'privacy_policy.html', {
        'page_title': 'Privacy Policy'
    })


def error_400(request, exception):
    LOGGER.error(f'404 Request: {request} Exception: {exception}')
    if request.method == 'POST':
        return HttpResponse(exception, status=400)

    return render(request, 'error_400.html', {
        'page_title': '400 Error',
        'exception': exception
    }, status=400)


def error_403(request, exception):
    LOGGER.error(f'403 Request: {request} Exception: {exception}')
    if request.method == 'POST':
        return HttpResponse(exception, status=403)

    return render(request, 'error_403.html', {
        'page_title': '403 Error',
        'exception': exception
    }, status=403)


def error_404(request, exception):
    LOGGER.error(f'404 Request: {request} Exception: {exception}')
    if request.method == 'POST':
        return HttpResponse(exception, status=404)

    return render(request, 'error_404.html', {
        'page_title': '404 Error',
        'exception': exception
    }, status=404)


def error_500(request):
    LOGGER.error(f'500 Request: {request}')
    if request.method == 'POST':
        return HttpResponse('There was an error processing your request.', status=500)

    return render(request, 'error_500.html', {
        'page_title': '500 Error'
    }, status=500)
