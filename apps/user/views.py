import boto3
import calendar
import os
import requests

from datetime import date

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Sum, Q, ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.administration.models import MAVP, ActionLog
from apps.api.models import ControllerSession
from apps.feedback.models import Feedback
from .forms import (
    AddMavpForm,
    EditProfileForm,
    EditUserForm,
    VisitingRequestForm,
    ManualAddVisitorForm
)
from apps.training.models import TrainingTicket
from apps.user.models import User, VisitRequest
from apps.user.update import add_visitor
from util.email import send_visitor_approval_email
from zid_web.decorators import require_staff, require_member, require_session


def view_roster(request):
    # TODO: Add select box to choose sort method
    sort = request.GET.get('sort', 'first_name')
    if sort not in ['first_name', 'last_name', 'rating']:
        return HttpResponse(status=400)

    home_roster = User.objects.filter(
        main_role='HC',
        status=0
    ).values(
        'first_name',
        'last_name',
        'cid',
        'oper_init',
        'rating',
        'staff_role',
        'training_role',
        'del_cert', 'gnd_cert', 'twr_cert', 'app_cert', 'ctr_cert'
    ).order_by(sort)

    visit_roster = User.objects.filter(
        main_role='VC',
        status=0
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
    ).order_by(sort)

    mavp_roster = User.objects.filter(
        main_role='MC',
        status=0
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
    ).order_by(sort)

    visitor_form = ManualAddVisitorForm()

    return render(request, 'roster.html', {
        'page_title': 'Roster',
        'home_roster': home_roster,
        'visit_roster': visit_roster,
        'mavp_roster': mavp_roster,
        'visitor_form': visitor_form
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

    hours_month = ControllerSession.objects.filter(
        start__year=year,
        start__month=month
    ).aggregate(
        duration=Sum('duration')
    )['duration']

    hours_year = ControllerSession.objects.filter(
        start__year=year
    ).aggregate(
        duration=Sum('duration')
    )['duration']

    hours_total = ControllerSession.objects.aggregate(
        duration=Sum('duration')
    )['duration']

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
        'year': year,
        'hours_month': hours_month,
        'hours_year': hours_year,
        'hours_total': hours_total
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

        ActionLog(
            action=f'{request.user_obj.full_name} added an MAVP agreement with {request.POST["facility_short"]}.'
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

        ActionLog(
            action=f'{request.user_obj.full_name} removed the MAVP agreement with {facility}.'
        ).save()

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
    if not (request.user_obj.cid == cid or request.user_obj.is_staff or request.user_obj.is_trainer):
        # Non-staff/trainer members should only be able to view their own profile
        return HttpResponse(status=403)
    try:
        user = User.objects.get(
            cid=cid
        )
    except ObjectDoesNotExist:
        raise Http404()

    form = EditUserForm(initial={
        'delivery': user.del_cert,
        'ground': user.gnd_cert,
        'tower': user.twr_cert,
        'approach': user.app_cert,
        'center': user.ctr_cert
    })

    # training_sessions = TrainingTicket.objects.filter(
    #     student=user
    # ).order_by('-session_date')

    response = requests.get(
        f'https://api.vatusa.net/v2/user/{cid}/training/records',
        params={
            'apikey': os.getenv('API_KEY')
        }
    )

    if response.status_code == 200:
        training_sessions = sorted(response.json()['data'], key=lambda k: k['session_date'], reverse=True)
        training_sessions = filter(lambda session: session['facility_id'] == 'ZID', training_sessions)
    else:
        training_sessions = []

    sessions = ControllerSession.objects.filter(user=user)
    now = timezone.now()
    stats = sessions.aggregate(
        month=Sum('duration', filter=Q(start__month=now.month) & Q(start__year=now.year)),
        year=Sum('duration', filter=Q(start__year=now.year))
    )

    feedback = Feedback.objects.filter(
        controller__cid=cid,
        status=1
    ).order_by('-last_updated')

    return render(request, 'profile.html', {
        'page_title': 'Profile',
        'user': user,
        'stats': stats,
        'form': form,
        'feedback': feedback,
        'training_sessions': training_sessions
    })


@require_member
def edit_profile(request, cid):
    if not (request.user_obj.cid == cid or request.user_obj.is_staff):
        return HttpResponse(status=403)
    try:
        user = User.objects.get(
            cid=cid
        )
    except ObjectDoesNotExist:
        raise Http404()

    # TODO: Add option to remove profile picture
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

        if request.user_obj.cid == cid:
            ActionLog(
                action=f'{request.user_obj.full_name} made changes to their profile.'
            ).save()
        else:
            ActionLog(
                action=f'{request.user_obj.full_name} made changes to {user.full_name}\'s profile.'
            ).save()

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
    try:
        user = User.objects.get(
            cid=cid
        )
    except ObjectDoesNotExist:
        raise Http404()

    if request.POST['oper_init']:
        if len(request.POST['oper_init']) is not 2:
            return HttpResponse('Operating initials must be 2 characters long!', status=404)
        user.oper_init = request.POST['oper_init']

    user.del_cert = request.POST['delivery']
    user.gnd_cert = request.POST['ground']
    user.twr_cert = request.POST['tower']
    user.app_cert = request.POST['approach']
    user.ctr_cert = request.POST['center']

    user.save()

    ActionLog(
        action=f'{request.user_obj.full_name} made changes to the endorsements for {user.full_name}.'
    ).save()

    return redirect(f'/profile/{cid}')


@require_session
def view_visit_request(request):
    if request.method == 'POST':
        VisitRequest(
            cid=request.POST['cid'],
            description=request.POST['description']
        ).save()

        return redirect('/?m=6')
    else:
        form = VisitingRequestForm(initial={
            'cid': request.session['cid'],
            'name': request.session['vatsim_data']['personal']['name_full'],
            'email': request.session['vatsim_data']['personal']['email'],
            'rating': request.session['vatsim_data']['vatsim']['rating']['short']
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

    try:
        req = VisitRequest.objects.get(cid=cid)
        req.status = 1
        req.save()
    except ObjectDoesNotExist:
        raise Http404()

    ActionLog(
        action=f'{request.user_obj.full_name} approved the visit request for {User.objects.get(cid=cid).full_name}.'
    ).save()

    send_visitor_approval_email(cid, request.user_obj.full_name)
    return redirect('/visit-request/manage')


@require_staff
def deny_visit_request(request, cid):
    try:
        req = VisitRequest.objects.get(cid=cid)
        req.status = 2
        req.save()
    except ObjectDoesNotExist:
        raise Http404()

    ActionLog(
        action=f'{request.user_obj.full_name} denied the visit request for {User.objects.get(cid=cid).full_name}.'
    ).save()
    # TODO: Add denial email logic
    return redirect('/visit-request/manage')


@require_staff
@require_POST
def manual_add_visitor(request):
    add_visitor(request.POST['cid'])
    send_visitor_approval_email(request.POST['cid'], "Test Sender")
    ActionLog(
        action=f'{request.user_obj.full_name} manually added {User.objects.get(cid=request.POST["cid"]).full_name} '
               f'as a visiting controller.'
    )
    return redirect('/roster')
