from django import template
from babel.dates import format_date, format_datetime, format_timedelta, format_time
from datetime import datetime, timedelta
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import markdown as mkdown

register = template.Library()

@register.filter(name='formatElbiralas')
def formatElbiralas(str: str) -> str:
    if str == "fuggo":
        return "Függőben"
    elif str == "elfogadott":
        return "Elfogadva"
    elif str == "elutasitott":
        return "Elutasítva"

@register.filter(name='ehn')
def ehn(datum):
    return format_datetime(datum, "yyyy.MM.dd EEEE", locale='hu_HU')

@register.filter(name='ehnop')
def ehnop(datum):
    return format_datetime(datum, "yyyy.MM.dd E hh:mm", locale='hu_HU')

@register.filter(name='ehnopegesz')
def ehnopegesz(datum):
    return format_datetime(datum, "yyyy.MM.dd E HH:mm", locale='hu_HU')

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
    delta = (datum.date().isocalendar()[1] - ma.isocalendar()[1])
    
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
        return f"{datum.date().isocalendar()[1]}. hét"
    else:
        return f"{datum.date().year}/{datum.date().isocalendar()[1]}. hét"

@register.filter(name='kozszolg_ido')
def kozszolg_ido(percek):
    return f"{percek // 60} óra {percek % 60} perc" if percek % 60 > 0 else f"{percek // 60} óra" if percek > -1 else ""

@register.filter(name='markdown')
@stringfilter
def markdown(value):
    md = mkdown.Markdown(extensions=['extra', 'smarty', 'fenced_code', 'codehilite'])
    return mark_safe(md.convert(value))