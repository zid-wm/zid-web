import calendar

from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Sum

from administration.models import MAVP
from api.models import ControllerSession
from .forms import AddMavpForm
from user.models import User
from zid_web.decorators import require_staff


def view_roster(request):
    home_roster = User.objects.filter(
        main_role='HC'
    ).values(
        'first_name',
        'last_name',
        'oper_init',
        'rating',
        'staff_role',
        'training_role',
        'del_cert', 'gnd_cert', 'twr_cert', 'app_cert', 'ctr_cert'
    ).order_by('last_name')

    visit_roster = User.objects.filter(
        main_role='VC'
    ).values(
        'first_name',
        'last_name',
        'oper_init',
        'home_facility',
        'rating',
        'staff_role',
        'training_role',
        'del_cert', 'gnd_cert', 'twr_cert', 'app_cert', 'ctr_cert'
    ).order_by('last_name')

    mavp_roster = User.objects.filter(
        main_role='MC'
    ).values(
        'first_name',
        'last_name',
        'oper_init',
        'home_facility',
        'rating',
        'staff_role',
        'training_role',
        'del_cert', 'gnd_cert', 'twr_cert', 'app_cert', 'ctr_cert'
    ).order_by('last_name')

    return render(request, 'roster.html', {
        'page_title': 'Roster',
        'home_roster': home_roster,
        'visit_roster': visit_roster,
        'mavp_roster': mavp_roster
    })


def view_staff(request):
    atm = User.objects.filter(staff_role='ATM', main_role='HC').first()
    datm = User.objects.filter(staff_role='DATM', main_role='HC').first()
    ta = User.objects.filter(staff_role='TA', main_role='HC').first()
    ec = User.objects.filter(staff_role='EC', main_role='HC').first()
    fe = User.objects.filter(staff_role='FE', main_role='HC').first()
    wm = User.objects.filter(staff_role='WM', main_role='HC').first()

    return render(request, 'staff.html', {
        'page_title': 'Staff',
        'atm': atm,
        'datm': datm,
        'ta': ta,
        'ec': ec,
        'fe': fe,
        'wm': wm
    })


def view_statistics(request):
    now = date.today()

    month = now.month
    year = now.year

    stats = ControllerSession.objects.filter(
        user__main_role='HC',
        start__year=year,
        start__month=month
    ).values(
        'user',
        'user__first_name',
        'user__last_name',
        'user__rating'
    ).annotate(
        duration=Sum('duration')
    ).order_by('user__last_name')

    return render(request, 'statistics.html', {
        'page_title': 'Statistics',
        'stats': stats,
        'month': calendar.month_name[month],
        'year': year
    })


@require_staff
def view_mavp(request):
    mavps = MAVP.objects.all()
    form = AddMavpForm()

    if request.method == 'POST':
        MAVP(
            facility_short=request.POST['facility_short'],
            facility_long=request.POST['facility_long']
        ).save()

    return render(request, 'mavp.html', {
        'page_title': 'MAVP Management',
        'mavps': mavps,
        'form': form
    })


@require_staff
def view_remove_mavp(request, facility):
    if request.method == 'POST':
        MAVP.objects.filter(
            facility_short=facility
        ).delete()

        User.objects.filter(
            main_role='MC',
            home_facility=facility
        ).delete()

        return redirect('/mavp')
    else:
        facility = MAVP.objects.get(
            facility_short=facility
        )

        return render(request, 'mavp-remove.html', {
            'page_title': 'Remove MAVP',
            'facility': facility
        })
