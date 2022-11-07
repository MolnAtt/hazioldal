from django import template
from datetime import datetime, timezone
from babel.dates import format_date, format_datetime, format_timedelta, format_time

register = template.Library()

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
    return format_timedelta(td, "HH:mm", locale='hu_HU')




@register.filter(name='lejart')
def lejart(datum):
    return datum < datetime.now(timezone.utc)


@register.filter(name='hatravan')
def hatravan(datum):
    result = ""
    kulonbseg = datum-datetime.now(timezone.utc)
    napok = kulonbseg.days
    orak = int(kulonbseg.seconds/3600)
    percek = int(kulonbseg.seconds/60%60)+1
    
    """
    variációk:
        nap-óra
        nap-perc
        nap
        óra-perc
        óra
        perc
    """

    if 0 < napok:
        result = f"{napok} nap "
        if 0 < orak:
            result += f"{orak} óra "
        elif 0 < percek:
            result += f"{percek} perc "
    elif 0 < orak: 
        result = f"{orak} óra "
        if 0 < percek:
            result += f"{percek} perc "
    elif 0 < percek:
         result = f"{percek} perc "

    return result


def ejfel(datum):
    return datum.hour == 0 and datum.minute == 0

@register.filter(name='pontosit')
def pontosit(datum):
    result = ""
    napkulonbseg = datum.day - datetime.now(timezone.utc).day

    """
    variációk: 

    tegnap (különbség -1):
        "tegnap, HH:mm"

    ma (különbség 0):
        "ma, HH:mm"
        kivéve 00:00, mert akkor "tegnap éjfél"

    holnap (különbség 1):
        "holnap, HH:mm"
        kivéve 00:00, mert akkor "ma éjfél"

    midig máskor:
        "november 11"
        kivéve különbség 2 és 00:00, mert akkor "holnap éjfél"
    """

    if napkulonbseg == -1:
        result = f'tegnap, {format_datetime(datum, "HH:mm")}'
    elif napkulonbseg == 0:
        if ejfel(datum):
            result = 'tegnap éjfél'
        else:
            result = f'ma, {format_datetime(datum, "HH:mm")}'
    elif napkulonbseg == 1:
        if ejfel(datum):
            result = 'ma éjfél'
        else:
            result = f'holnap, {format_datetime(datum, "HH:mm")}'
    else:
        if napkulonbseg == 2 and ejfel(datum):
            result = 'holnap éjfél'
        else:
            result = format_datetime(datum, "MMM dd, EEEE", locale='hu_HU')

    return result