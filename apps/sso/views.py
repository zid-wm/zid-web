import json
import logging
import os
import requests
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import redirect


LOGGER = logging.getLogger(__name__)


def login_start(request):
    query_string = (
        f'?client_id={os.getenv("VATSIM_CLIENT_ID")}'
        f'&redirect_uri={os.getenv("VATSIM_REDIRECT_URI")}'
        f'&response_type=code'
        f'&scope={os.getenv("VATSIM_SCOPE")}'
    )
    query_params = urllib.parse.quote_plus(query_string, safe='?&=')

    return redirect(
        os.getenv('VATSIM_AUTH_URL') + query_params
    )


def login(request):
    error_string = 'Something went wrong with VATSIM login! Please try again later.'
    if request.GET.get('code', False):
        post_body = {
            'grant_type': 'authorization_code',
            'client_id': os.getenv('VATSIM_CLIENT_ID'),
            'client_secret': os.getenv('VATSIM_CLIENT_SECRET'),
            'redirect_uri': os.getenv('VATSIM_REDIRECT_URI'),
            'code': request.GET.get('code')
        }
        response = requests.post(os.getenv('VATSIM_TOKEN_URL'), post_body)

        if response.ok:
            data = json.loads(response.text)
            request.session['token_data'] = data

            user_response = requests.get(os.getenv('VATSIM_USER_URL'), headers={
                'Authorization': f'Bearer {data["access_token"]}',
                'Accept': 'application/json'
            })

            if user_response.ok:
                user_data = json.loads(user_response.text)['data']
                request.session['vatsim_data'] = user_data
                request.session['cid'] = user_data['cid']
            else:
                LOGGER.error('User response not ok!')
                LOGGER.error('Response: %s', user_response)
                return HttpResponse(error_string, status=500)
        else:
            LOGGER.error('VATSIM token response not ok!')
            LOGGER.error('Response: %s', response)
            return HttpResponse(error_string, status=500)
        return redirect(request.session.pop('redirect_after_login', '/?m=5'))
    else:
        LOGGER.error('Parameter \'code\' not present in login request.')
        return HttpResponse(error_string, status=500)


def logout(request):
    request.session.flush()
    return redirect("/?m=4")