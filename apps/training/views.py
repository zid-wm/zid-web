import os
import requests

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.administration.models import ActionLog
from apps.training.forms import TrainingTicketForm
from apps.training.models import TrainingTicket
from apps.user.models import User
from zid_web.decorators import require_staff_or_mentor, require_member


@require_staff_or_mentor
def view_training_hub(request):
    trainers = User.objects.filter(
        training_role__in=['INS', 'MTR'],
        main_role='HC'
    ).order_by('last_name')

    session_query = TrainingTicket.objects.all().order_by('-session_date')
    paginator = Paginator(session_query, per_page=10)
    page_num = request.GET.get('p')
    page = paginator.get_page(page_num)

    if not page_num:
        page_num = 1

    return render(request, 'training-hub.html', {
        'page_title': 'Training Hub',
        'trainers': trainers,
        'sessions': page,
        'page_num': page_num,
        'has_next': page.has_next(),
        'has_previous': page.has_previous()
    })


@require_member
def view_ticket_details(request, ticket_id):
    ticket = TrainingTicket.objects.get(
        id=ticket_id
    )

    if not (
            request.user_obj.is_staff
            or request.user_obj.is_trainer
            or request.user_obj.cid == ticket.student.cid
    ):
        return HttpResponse(status=403)

    return render(request, 'ticket-details.html', {
        'page_title': 'Ticket Details',
        'ticket': ticket
    })


def post_training_ticket(ticket, data, student, instructor):
    post_data = {
        'instructor_id': instructor.cid,
        'session_date': data['session_date'],
        'position': data['position'],
        'duration': data['session_duration'],
        'movements': int(data['movements']),
        'score': int(data['score']),
        'notes': data['notes'],
        'location': int(data['location']),
        'ots_status': int(data['ots_status']),
        'solo_granted': 'solo_granted' in data
    }

    url = f'https://api.vatusa.net/v2/user/{student.cid}/training/record'

    response = requests.post(url, post_data, params={
        'apikey': os.getenv('API_KEY')
    }).json()

    if response['status'] == 'OK':
        ticket.vatusa_id = response['id']
        return True
    else:
        print(response)
        return False


@require_staff_or_mentor
def submit_training_ticket(request):
    if request.method == 'POST':
        student = User.objects.get(
            cid=request.POST['student']
        )

        print(request.POST)
        data = request.POST

        ticket = TrainingTicket(
            student=student,
            instructor=request.user_obj,
            session_date=data['session_date'],
            position=data['position'],
            session_duration=data['session_duration'],
            movements=int(data['movements']),
            score=int(data['score']),
            notes=data['notes'],
            location=int(data['location']),
            ots_status=int(data['ots_status']),
            solo_granted='solo_granted' in data
        )

        if post_training_ticket(ticket, data, student, request.user_obj):
            ticket.save()
            ActionLog(action=f'{request.user_obj.full_name} created a new training ticket for {student.full_name}.')
            return redirect('/training')

        else:
            return HttpResponse('Error posting ticket to VATUSA API!', status=500)
    else:
        form = TrainingTicketForm

        return render(request, 'submit-ticket.html', {
            'page_title': 'Submit Training Ticket',
            'form': form
        })
