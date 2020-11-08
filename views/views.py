import requests
import os

from datetime import date
from django.shortcuts import render
from django.db.models import Sum, Q

from api.models import Controller, ControllerSession
from user.models import User


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
    total_home_controllers = User.objects.filter(main_role='HC').count()
    month_control_time = str(ControllerSession.objects.aggregate(
        Sum('duration'))['duration__sum']).split('.')[0]

    try:
        # The timeout is set to slightly longer than a standard TCP packet retransmission window.
        pilots = requests.get('https://api.denartcc.org/live/ZID', timeout=3.05).json()
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
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

    dev_env = os.getenv('DEV_ENV')

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
        'dev_env': dev_env
    })
