import os
import re

from django import template

from apps.feedback.forms import SERVICE_LEVEL_CHOICES
from apps.user.models import ENDORSEMENTS

register = template.Library()


@register.filter
def format_duration(td):
    """
    The native Django datetime field returns timestamps in the format:
    DD days, HH:MM:SS.XXXXXX
    This function chops off the seconds and changes the number of days
    to appear as colon-delimited.
    """
    if td:
        time = re.findall(r'\d+', str(td))
        if len(time) == 4:  # then there is a day value
            result = f'{(int(time[0]) * 24) + int(time[1])}:{time[2]}'
        else:
            result = f'{time[0]}:{time[1]}'
        return result
    else:
        return '0:00'


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


@register.filter
def ots_display(n):
    display_text = {
        0: "No OTS",
        1: "OTS Pass",
        2: "OTS Fail",
        3: "OTS Recommended"
    }
    return display_text[n]


@register.filter
def training_score_display(n):
    display_text = {
        1: "No Progress",
        2: "Little Progress",
        3: "Average Progress",
        4: "Great Progress",
        5: "Exceptional Progress"
    }
    return display_text[n]


@register.simple_tag
def uls_redirect_url():
    return os.getenv('ULS_REDIR_URL')


@register.filter
def lookup(dict, key):
    return dict.get(key)
