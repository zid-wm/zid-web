from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from apps.administration.forms import SendEmailForm
from apps.administration.models import ActionLog
from apps.user.models import User
from util.email.email import send_broadcast_email
from zid_web.decorators import require_staff


@require_staff
def view_audit_log(request):
    log_results = ActionLog.objects.all().order_by('-timestamp')

    paginator = Paginator(log_results, per_page=50)
    page_num = request.GET.get('p')
    page = paginator.get_page(page_num)

    return render(request, 'auditlog.html', {
        'page_title': 'Audit Log',
        'log_items': page,
        'page_num': page_num,
        'has_next': page.has_next(),
        'has_previous': page.has_previous()
    })


@require_staff
def view_send_email(request):
    if request.method == 'POST':
        if 'TRAIN' in request.POST.getlist('controllers'):
            emails = list(User.objects.filter(
                training_role__isnull=False,
                main_role='HC'
            ).values('email'))
        else:
            emails = list(User.objects.filter(
                main_role__in=request.POST.getlist('controllers'),
                rating__in=request.POST.getlist('ratings')
            ).values('email'))

        send_broadcast_email(
            request,
            request.POST['subject'],
            request.POST['message'],
            request.POST['reply_email'],
            emails
        )
        return redirect('/')
    else:
        form = SendEmailForm(request)
        return render(request, 'send_email.html', {
            'page_title': 'Send Email',
            'form': form
        })
