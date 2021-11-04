from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from apps.administration.models import ActionLog
from apps.feedback.forms import NewFeedbackForm, ReviewFeedbackForm
from apps.feedback.models import Feedback
from apps.user.models import User
from zid_web.decorators import require_staff


def new_feedback(request):
    form = NewFeedbackForm()
    return render(request, 'feedback.html', {
        'page_title': 'Submit Feedback',
        'form': form
    })


@require_POST
def submit_feedback(request):
    feedback = Feedback(
        controller=User.objects.get(
            cid=request.POST['controller']
        ),
        position=request.POST['position'],
        service_level=request.POST['service_level'],
        flight_callsign=request.POST['flight_callsign'],
        pilot_name=request.POST['pilot_name'],
        pilot_email=request.POST['pilot_email'],
        pilot_cid=request.POST['pilot_cid'],
        additional_comments=request.POST['additional_comments']
    )

    feedback.save()
    return redirect('/?m=2')


@require_staff
def manage_feedback(request):
    feedback = Feedback.objects.all().order_by('-submitted')
    return render(request, 'manage-feedback.html', {
        'page_title': 'Manage Feedback',
        'feedback': feedback
    })


@require_staff
def post_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
    except ObjectDoesNotExist:
        raise Http404()

    if request.method == 'POST':
        feedback.staff_comment = request.POST['staff_comment']
        feedback.status = 1
        feedback.save()

        ActionLog(
            action=f'Feedback {feedback.id} for {feedback.controller.full_name} '
                   f'was posted by {request.user_obj.full_name}.'
        ).save()

        return redirect('/feedback/manage')

    else:
        form = ReviewFeedbackForm()
        return render(request, 'post-feedback.html', {
            'page_title': 'Post Feedback',
            'feedback': feedback,
            'form': form
        })


@require_staff
def reject_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
    except ObjectDoesNotExist:
        raise Http404()
    if request.method == 'POST':
        feedback.staff_comment = request.POST['staff_comment']
        feedback.status = 2
        feedback.save()

        ActionLog(
            action=f'Feedback {feedback.id} for {feedback.controller.full_name} '
                   f'was rejected by {request.user_obj.full_name}.'
        ).save()

        return redirect('/feedback/manage')
    else:
        form = ReviewFeedbackForm()
        return render(request, 'reject-feedback.html', {
            'page_title': 'Reject Feedback',
            'feedback': feedback,
            'form': form
        })
