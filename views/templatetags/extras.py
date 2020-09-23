from django import template


register = template.Library()


@register.filter
def format_duration(td):
    return str(td).split('.')[0]