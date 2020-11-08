import os

from django import template

register = template.Library()


@register.filter
def format_duration(td):
    return str(td).split('.')[0]


@register.simple_tag
def uls_redirect_url():
    return os.getenv('ULS_REDIR_URL')
