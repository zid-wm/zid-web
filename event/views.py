import boto3

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from event.models import Event, EventPosition, EventSignup
from .forms import NewEventForm, AddPositionForm, EditEventForm
from user.models import User
from zid_web.decorators import require_staff, require_member


def view_events(request):
    events = Event.objects.filter(
        end__gte=timezone.now()
    ).order_by('start')

    return render(request, 'events.html', {
        'page_title': 'Events',
        'heading': 'Events',
        'events': events
    })


def view_event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user_obj

    add_position_form = AddPositionForm()

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
            'position_signups': position_signups
        })

    else:
        return HttpResponse(status=403)


@require_staff
def view_archived_events(request):
    events = Event.objects.filter(
        end__lte=timezone.now()
    ).order_by('start')

    return render(request, 'events.html', {
        'page_title': 'Archived Events',
        'heading': 'Archived Events',
        'events': events
    })


@require_staff
def view_new_event(request):
    form = NewEventForm()

    if request.method == 'POST':
        # TODO: Add a check that the title doesn't match an existing event

        s3 = boto3.client('s3')
        s3.upload_fileobj(
            request.FILES['banner'],
            'zid-files',
            f'img/{request.POST["name"]}',
            ExtraArgs={
                'ACL': 'public-read'
            }
        )

        new_event = Event(
            name=request.POST['name'],
            banner=f'https://zid-files.s3.us-east-1.amazonaws.com/img/{request.POST["name"]}',
            start=request.POST['start'],
            end=request.POST['end'],
            host=request.POST['host'],
            description=request.POST['description']
        )
        new_event.save()
        return redirect('/events')

    else:
        return render(request, 'new-event.html', {
            'page_title': 'New Event',
            'form': form
        })


@require_staff
def edit_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(
            id=event_id
        )

        event.name = request.POST['name']
        event.start = request.POST['start']
        event.end = request.POST['end']
        event.host = request.POST['host']
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
        return redirect('/events')
    else:
        event = Event.objects.get(
            id=event_id
        )

        form = EditEventForm(initial={
            'name': event.name,
            'start': event.start,
            'end': event.end,
            'host': event.host,
            'description': event.description
        })

        return render(request, 'edit-event.html', {
            'page_title': 'Edit Event',
            'event': event,
            'form': form
        })


@require_staff
def delete_position(request, position_id, event_id):
    EventPosition.objects.get(id=position_id).delete()
    return redirect(f'/events/{event_id}')


@require_staff
def delete_event(request, event_id):
    Event.objects.get(id=event_id).delete()
    return redirect(f'/events')


@require_member
def request_position(request, event_id, pos_id):
    signup = EventSignup(
        position=EventPosition.objects.get(
            id=pos_id
        ),
        user=User.objects.get(
            cid=request.user_obj.cid
        )
    )
    signup.save()
    return redirect(f'/events/{event_id}')
