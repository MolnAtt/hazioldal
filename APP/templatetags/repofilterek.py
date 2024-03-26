from django import template
from babel.dates import format_date, format_datetime, format_timedelta, format_time
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='ehn')
def ehn(datum):
    return format_datetime(datum, "yyyy.MM.dd EEEE", locale='hu_HU')

@register.filter(name='ehnop')
def ehnop(datum):
    return format_datetime(datum, "yyyy.MM.dd E hh:mm", locale='hu_HU')

@register.filter(name='ehnopegesz')
def ehnopegesz(datum):
    return format_datetime(datum, "yyyy.MM.dd E HH:MM", locale='hu_HU')

@register.filter(name='hnop')
def hnop(datum):
    return format_datetime(datum, "MMM dd. E hh:mm", locale='hu_HU')

@register.filter(name='hn')
def hn(datum):
    return format_datetime(datum, "MMMM dd.", locale='hu_HU')

@register.filter(name='op')
def op(td):
    return format_timedelta(td, "HH:MM", locale='hu_HU')

@register.filter(name='day_relative')
def day_relative(datum):
    ma = datetime.now().date()
    delta = datum.date() - ma

    if delta.days == 0:
        return 'Ma'
    elif delta.days == -1:
        return 'Tegnap'
    elif delta.days == 1:
        return 'Holnap'
    elif delta.days == -2:
        return 'Tegnapelőtt'
    elif delta.days == 2:
        return 'Holnapután'
    elif datum.date().year == ma.year:
        return format_datetime(datum, "MMMM dd.", locale='hu_HU')
    else:
        return format_datetime(datum, "yyyy. MMMM dd.", locale='hu_HU')
    
@register.filter(name='week_relative')
def week_relative(datum:datetime):
    ma = datetime.now().date()
    delta = (datum.date().isocalendar().week - ma.isocalendar().week)
    
    if delta == 0:
        return 'Ez a hét'
    elif delta == -1:
        return 'Előző hét'
    elif delta == -2:
        return 'Két hete'
    elif delta == 1:
        return 'Jövő hét'
    elif delta == 2:
        return "Két hét múlva"
    elif datum.date().year == ma.year:
        return f"{datum.date().isocalendar().week}. hét"
    else:
        return f"{datum.date().year}/{datum.date().isocalendar().week}. hét"