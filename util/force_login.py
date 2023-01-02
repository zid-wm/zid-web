from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect


def force_login(request: HttpRequest):
    try:
        protocol = 'https://' if request.META['SERVER_PORT'] == 443 else 'http://'
        redirect_url = protocol + request.META['HTTP_HOST'] + request.META['PATH_INFO']
    except KeyError:
        redirect_url = '/'

    request.session['redirect_after_login'] = redirect_url
    return HttpResponseRedirect('/login-start')
