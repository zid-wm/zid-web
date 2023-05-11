from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.administration.forms import SendEmailForm, StaffCommentForm
from apps.administration.models import ActionLog, StaffComment
from apps.user.models import User
from util.email import send_broadcast_email
from zid_web.decorators import require_staff, require_role


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
        return redirect('/?m=3')
    else:
        form = SendEmailForm(request)
        return render(request, 'send_email.html', {
            'page_title': 'Send Email',
            'form': form
        })


@require_role(['ATM', 'DATM', 'TA', 'WM'])
def view_add_staff_comment(request, subject_cid):
    if request.method == 'GET':
        if not User.objects.filter(cid=subject_cid).exists():
            return HttpResponse(f'User with CID {subject_cid} not found!', status=404)
        user = User.objects.get(cid=subject_cid)
        form = StaffCommentForm(user.full_name)
        return render(request, 'add_staff_comment.html', {
            'page_title': 'Add Staff Comment',
            'form': form,
            'subject_cid': subject_cid,
            'user': user
        })

    elif request.method == 'POST':
        StaffComment(
            writer=User.objects.get(cid=request.user_obj.cid),
            subject=User.objects.get(cid=subject_cid),
            notes=request.POST['notes']
        ).save()
        return redirect('/?m=8')


@require_role(['ATM', 'DATM', 'TA', 'WM'])
def view_delete_staff_comment(request, comment_id):
    if StaffComment.objects.filter(id=comment_id).exists():
        comment = StaffComment.objects.get(id=comment_id)
        if comment.writer.cid == request.user_obj.cid:
            comment.delete()
            return redirect('/?m=9')
        else:
            return HttpResponse('You are not permitted to delete another staff member\'s notes!', status=403)
    else:
        return redirect('/?m=10')
