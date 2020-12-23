import os
import re

from django import template

from feedback.models import SERVICE_LEVEL_CHOICES
from user.models import ENDORSEMENTS

register = template.Library()


@register.filter
def format_duration(td):
    """
    The native Django datetime field returns timestamps in the format:
    DD days, HH:MM:SS.XXXXXX
    This function chops off the seconds and changes the number of days
    to appear as colon-delimited.
    """
    time = re.findall(r'\d+', str(td))
    hours = (int(time[0]) * 24) + int(time[1])
    minutes = time[2]
    return f'{hours}:{minutes}'


@register.filter
def endorsement(e):
    for choice in ENDORSEMENTS:
        if choice[0] == e:
            return choice[1]
    return ''


@register.filter
def feedback(f):
    for choice in SERVICE_LEVEL_CHOICES:
        if choice[0] == f:
            return choice[1]
    return ''


@register.simple_tag
def uls_redirect_url():
    return os.getenv('ULS_REDIR_URL')


@register.filter
def lookup(dict, key):
    return dict.get(key)
