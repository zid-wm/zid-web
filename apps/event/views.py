import boto3
import logging
from datetime import datetime

from django.db.models import Q, ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.administration.models import ActionLog
from apps.event.models import Event, EventPosition, EventSignup
from .forms import EventForm, AddPositionForm
from apps.user.models import User
from zid_web.decorators import require_staff, require_member


LOGGER = logging.getLogger(__name__)


def view_events(request):
    new_event_form = EventForm()

    if 'archive' in request.path:
        heading = 'Archived'

        events = Event.objects.filter(
            end__lte=timezone.now()
        ).order_by('start')
    else:
        heading = 'Upcoming'

        events = Event.objects.filter(
            end__gte=timezone.now()
        ).order_by('start')

    return render(request, 'events.html', {
        'page_title': 'Events',
        'heading': heading,
        'events': events,
        'new_event_form': new_event_form
    })


def view_event_details(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise Http404()

    user = request.user_obj

    user_has_position = EventPosition.objects.filter(
        user=user,
        event=event
    ).exists()

    requested_positions = [
        signup.position.callsign for signup in EventSignup.objects.filter(
            user=user,
            position__event__id=event_id
        )
    ]

    add_position_form = AddPositionForm()

    edit_event_form = EventForm(initial={
        'name': event.name,
        'start': datetime.strftime(event.start, '%m/%d/%y %H:%M'),
        'end': datetime.strftime(event.end, '%m/%d/%y %H:%M'),
        'host': event.host,
        'description': event.description
    })

    if request.method == 'POST' and request.user_obj.is_staff:
        pos = EventPosition(
            callsign=request.POST['callsign'],
            event=event
        )
        pos.save()

    if event.hidden and user.is_staff or not event.hidden:
        positions = {'center': [], 'tracon': [], 'cab': []}
        position_signups = {}
        for position in event.positions.all():
            positions[position.category] += [position]

            position_signups[position.callsign] = EventSignup.objects.filter(
                position=position
            )

        return render(request, 'event-details.html', {
            'page_title': event.name,
            'event': event,
            'positions': positions,
            'available': {k: len(list(filter(lambda pos: pos.user is None, positions[k]))) for k in positions},
            'user': user,
            'allowed_to_signup': user and user.status == 'ACTIVE' and event.end >= timezone.now(),
            'add_position_form': add_position_form,
            'edit_event_form': edit_event_form,
            'position_signups': position_signups,
            'user_has_position': user_has_position,
            'requested_positions': requested_positions
        })

    else:
        return HttpResponse(status=403)


@require_staff
@require_POST
def view_new_event(request):
    if 'banner' in request.FILES:
        s3 = boto3.client('s3')
        s3.upload_fileobj(
            request.FILES['banner'],
            'zid-files',
            f'img/{request.POST["name"]}',
            ExtraArgs={
                'ACL': 'public-read'
            }
        )

    start_time = datetime.strptime(request.POST['start'], '%m/%d/%y %H:%M')
    end_time = datetime.strptime(request.POST['end'], '%m/%d/%y %H:%M')

    new_event = Event(
        name=request.POST['name'],
        banner=f'https://zid-files.s3.us-east-1.amazonaws.com/img/{request.POST["name"]}'
        if 'banner' in request.FILES else None,
        start=start_time,
        end=end_time,
        host=request.POST['host'],
        event_signup_type=request.POST['event_signup_type'],
        description=request.POST['description']
    )
    new_event.save()
    ActionLog(
        action=f'Event {request.POST["name"]} was created by {request.user_obj.full_name}.'
    ).save()
    return redirect(f'/events/{new_event.id}')


@require_staff
@require_POST
def edit_event(request, event_id):
    try:
        event = Event.objects.get(
            id=event_id
        )
    except ObjectDoesNotExist:
        raise Http404()

    event.name = request.POST['name']
    event.start = datetime.strptime(request.POST['start'], '%m/%d/%y %H:%M')
    event.end = datetime.strptime(request.POST['end'], '%m/%d/%y %H:%M')
    event.host = request.POST['host']
    event.event_signup_type = request.POST['event_signup_type']
    event.description = request.POST['description']

    if request.FILES:
        s3 = boto3.client('s3')
        s3.upload_fileobj(
            request.FILES['banner'],
            'zid-files',
            f'img/{request.POST["name"]}',
            ExtraArgs={
                'ACL': 'public-read'
            }
        )
        event.banner = f'https://zid-files.s3.us-east-1.amazonaws.com/img/{request.POST["name"]}'

    event.save()
    ActionLog(
        action=f'Event {request.POST["name"]} was edited by {request.user_obj.full_name}.'
    ).save()
    return redirect(f'/events/{event_id}')


@require_staff
def delete_position(request, position_id, event_id):
    try:
        EventPosition.objects.get(id=position_id).delete()
    except ObjectDoesNotExist:
        raise Http404()
    return redirect(f'/events/{event_id}')


@require_staff
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event_name = event.name
        event.delete()
    except Exception:
        raise Http404()
    ActionLog(
        action=f'Event {event_name} was deleted by {request.user_obj.full_name}.'
    ).save()
    return redirect(f'/events')


@require_member
def request_position(request, event_id, pos_id):
    try:
        event = Event.objects.get(
            id=event_id
        )

        signup = EventSignup(
            position=EventPosition.objects.get(
                id=pos_id
            ),
            user=User.objects.get(
                cid=request.user_obj.cid
            )
        )
        if event.event_signup_type == 'Open':
            signup.assign()
            ActionLog(
                action=f'{signup.user.full_name} signed up for '
                       f'{signup.position.callsign} for {signup.position.event.name}.'
            ).save()
        signup.save()

    except ObjectDoesNotExist:
        return HttpResponse(404)

    return redirect(f'/events/{event_id}')


@require_staff
def assign_position(request, signup_id):
    try:
        signup = EventSignup.objects.get(
            id=signup_id
        )
        signup.assign()
        signup.save()
    except ObjectDoesNotExist:
        raise Http404()

    ActionLog(
        action=f'{signup.user.full_name} was assigned to {signup.position.callsign} for {signup.position.event.name} '
               f'by {request.user_obj.full_name}.'
    ).save()

    EventSignup.objects.filter(
        Q(position=signup.position) |
        Q(user=signup.user)
    ).delete()

    return redirect(f'/events/{signup.position.event_id}')
