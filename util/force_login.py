from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect


def force_login(request: HttpRequest):
    try:
        redirect_url = request.path
    except KeyError:
        redirect_url = '/'

    request.session['redirect_after_login'] = redirect_url
    return HttpResponseRedirect('/login-start')
