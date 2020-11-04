import os
import hmac
import requests

from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.http import HttpResponse
from django.shortcuts import redirect
from user.models import User


def login(request):
    # Check if user has token from VATUSA
    if request.GET.get('token'):
        raw_token = request.GET['token']
        token = raw_token.split('.')
        token_sig = token[2]

        jwk_sig = urlsafe_b64encode(
            hmac.digest(
                urlsafe_b64decode(os.getenv('ULS_K_VALUE') + '=='),
                f'{token[0]}.{token[1]}'.encode(),
                'sha256'
            )
        )[:-1].decode()

        if token_sig == jwk_sig:
            data = requests.get(
                f'https://login.vatusa.net/uls/v2/info?token={token[1]}'
            ).json()

            request.session['vatsim_data'] = data
            request.session['cid'] = data['cid']
        else:
            return HttpResponse('Something was wrong with the token we got from VATUSA!', status=500)

    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')
