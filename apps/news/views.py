from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from apps.user.models import User
from zid_web.decorators import require_staff

from .forms import NewArticleForm
from .models import NewsArticle


def view_news(request):
    news = NewsArticle.objects.all().order_by('-date_posted')

    paginator = Paginator(news, per_page=10)
    page_num = request.GET.get('p')
    page = paginator.get_page(page_num)

    return render(request, 'news.html', {
        'page_title': 'News',
        'news': page,
        'page_num': page_num,
        'has_next': page.has_next(),
        'has_previous': page.has_previous()
    })


def view_article(request, article_id):
    try:
        article = NewsArticle.objects.get(id=article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'article.html', {
        'page_title': article.title,
        'article': article
    })


@require_staff
def view_submit_new_article(request):
    if request.method == 'POST':
        new_article = NewsArticle(
            title=request.POST['title'],
            content=request.POST['content'],
            author=User.objects.get(cid=request.user_obj.cid)
        )
        new_article.save()
        return redirect('/?m=7')
    else:
        form = NewArticleForm()

        return render(request, 'new-article.html', {
            'page_title': 'New Article',
            'form': form
        })


@require_staff
def delete_article(request, article_id):
    try:
        NewsArticle.objects.get(id=article_id).delete()
    except ObjectDoesNotExist:
        raise Http404()
    return redirect('/news')
