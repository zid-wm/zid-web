import boto3
import calendar
import os
import requests

from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Sum, Q
from django.utils import timezone
from django.views.decorators.http import require_POST

from administration.models import MAVP
from api.models import ControllerSession
from .forms import (
    AddMavpForm,
    EditProfileForm,
    EditEndorsementForm,
    VisitingRequestForm
)
from user.models import User, VisitRequest
from user.update import add_visitor
from zid_web.decorators import require_staff, require_member, require_session


def view_roster(request):
    home_roster = User.objects.filter(
        main_role='HC'
    ).values(
        'first_name',
        'last_name',
        'cid',
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
        'cid',
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
        'cid',
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


@require_member
def view_profile(request, cid):
    user = User.objects.get(
        cid=cid
    )

    form = EditEndorsementForm(initial={
        'delivery': user.del_cert,
        'ground': user.gnd_cert,
        'tower': user.twr_cert,
        'approach': user.app_cert,
        'center': user.ctr_cert
    })

    sessions = ControllerSession.objects.filter(user=user)
    now = timezone.now()
    stats = sessions.aggregate(
        month=Sum('duration', filter=Q(start__month=now.month) & Q(start__year=now.year)),
        year=Sum('duration', filter=Q(start__year=now.year))
    )

    return render(request, 'profile.html', {
        'page_title': 'Profile',
        'user': user,
        'stats': stats,
        'form': form
    })


@require_member
def edit_profile(request, cid):
    # TODO: Add check to verify user
    user = User.objects.get(
        cid=cid
    )
    if request.method == 'POST':
        if request.FILES:
            s3 = boto3.client('s3')
            s3.upload_fileobj(
                request.FILES['profile_pic'],
                'zid-files',
                f'profile/{cid}',
                ExtraArgs={
                    'ACL': 'public-read'
                }
            )

            user.profile_picture = f'https://zid-files.s3.us-east-1.amazonaws.com/profile/{cid}'

        if request.POST['biography']:
            user.biography = request.POST['biography']

        user.save()
        return redirect(f'/profile/{cid}')

    else:
        form = EditProfileForm(initial={
            'biography': user.biography
        })

        return render(request, 'edit-profile.html', {
            'page_title': 'Edit Profile',
            'form': form
        })


@require_staff
@require_POST
def edit_endorsements(request, cid):
    user = User.objects.get(
        cid=cid
    )

    user.del_cert = request.POST['delivery']
    user.gnd_cert = request.POST['ground']
    user.twr_cert = request.POST['tower']
    user.app_cert = request.POST['approach']
    user.ctr_cert = request.POST['center']

    user.save()

    return redirect(f'/profile/{cid}')


@require_session
def view_visit_request(request):
    if request.method == 'POST':
        VisitRequest(
            cid=request.POST['cid'],
            description=request.POST['description']
        ).save()

        return redirect('/')
    else:
        form = VisitingRequestForm(initial={
            'cid': request.session["vatsim_data"]["cid"],
            'name': f'{request.session["vatsim_data"]["firstname"]} {request.session["vatsim_data"]["lastname"]}',
            'email': request.session["vatsim_data"]["email"],
            'rating': request.session["vatsim_data"]["rating"],
            'facility': request.session['vatsim_data']['facility']['name']
        })

        return render(request, 'visit-request.html', {
            'page_title': 'Visit Request',
            'form': form
        })


@require_staff
def manage_visit_requests(request):
    reqs = VisitRequest.objects.all().order_by('-submitted')
    entries = []
    for req in reqs:
        controller_data = requests.get(
            f'https://api.vatusa.net/v2/user/{req.cid}',
            params={
                'apikey': os.getenv('API_KEY')
            }
        ).json()

        entries.append({
            'cid': req.cid,
            'name': f'{controller_data["fname"]} {controller_data["lname"]}',
            'email': controller_data["email"],
            'rating': controller_data["rating_short"],
            'home': controller_data["facility"],
            'submitted': req.submitted,
            'status_code': req.status,
            'status': VisitRequest.REQUEST_STATUSES[req.status][1]
        })

    return render(request, 'visit-request-manage.html', {
        'page_title': 'Manage Visiting Requests',
        'requests': entries
    })


@require_staff
def approve_visit_request(request, cid):
    add_visitor(cid)

    req = VisitRequest.objects.get(cid=cid)
    req.status = 1
    req.save()
    # TODO: Add approval email logic
    return redirect('/visit-request/manage')


@require_staff
def deny_visit_request(request, cid):
    req = VisitRequest.objects.get(cid=cid)
    req.status = 2
    req.save()
    # TODO: Add denial email logic
    return redirect('/visit-request/manage')
