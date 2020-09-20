from django.shortcuts import render


def view_home(request):
    return render(request, 'home.html', {
        'page_title': 'Home'
    })
