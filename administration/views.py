from django.core.paginator import Paginator
from django.shortcuts import render

from administration.models import ActionLog
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
