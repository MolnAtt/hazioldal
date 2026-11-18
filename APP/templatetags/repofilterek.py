from django import template
from babel.dates import format_date, format_datetime, format_timedelta, format_time
from datetime import datetime, timedelta
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import bleach
import markdown as mkdown

register = template.Library()

_ALLOWED_HTML_TAGS = {
    'a', 'b', 'blockquote', 'br', 'code', 'del', 'div', 'em', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'kbd', 'li', 'ol', 'p', 'pre',
    's', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot',
    'th', 'thead', 'tr', 'ul',
}

_ALLOWED_HTML_ATTRIBUTES = {
    'a': {'href', 'title'},
    'img': {'src', 'alt', 'title'},
    'code': {'class'},
    'div': {'class'},
    'span': {'class'},
    'pre': {'class'},
    'td': {'align'},
    'th': {'align'},
}

_ALLOWED_HTML_PROTOCOLS = {'http', 'https', 'mailto'}

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
    rendered = mkdown.Markdown(
        extensions=['extra', 'smarty', 'fenced_code', 'codehilite']
    ).convert(str(value))

    cleaned = bleach.clean(
        rendered,
        tags=_ALLOWED_HTML_TAGS,
        attributes=_ALLOWED_HTML_ATTRIBUTES,
        protocols=_ALLOWED_HTML_PROTOCOLS,
        strip=True,
    )
    return mark_safe(cleaned)