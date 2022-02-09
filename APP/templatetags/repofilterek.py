from django import template
from babel.dates import format_date, format_datetime, format_timedelta, format_time

register = template.Library()

@register.filter(name='ehn')
def ehn(datum):
    return format_datetime(datum, "yyyy.MM.dd EEEE", locale='hu_HU')

@register.filter(name='op')
def ehn(td):
    return format_timedelta(td, "HH:MM", locale='hu_HU')