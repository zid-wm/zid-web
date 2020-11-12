import os

from django import template

from user.models import ENDORSEMENTS

register = template.Library()


@register.filter
def format_duration(td):
    return str(td).split('.')[0]


@register.filter
def endorsement(e):
    for choice in ENDORSEMENTS:
        if choice[0] == e:
            return choice[1]
    return ''


@register.simple_tag
def uls_redirect_url():
    return os.getenv('ULS_REDIR_URL')
