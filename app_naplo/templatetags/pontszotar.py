import math
from django import template

register = template.Library()


@register.simple_tag(name='getget')
def getget(pontszotar, tanulo, feladat):
    if tanulo in pontszotar.keys() and feladat in pontszotar[tanulo].keys():
        ertek = pontszotar[tanulo][feladat]
        try:
            szamertek = float(ertek)
            if 0 <= szamertek:
                if szamertek==round(szamertek):
                    return int(szamertek) 
                return szamertek
            return ""
        except:
            return ertek
    return ""

@register.simple_tag(name='listaget')
def listaget(lista, i):
    try:
        return lista[i]
    except (IndexError, TypeError):
        return ""


@register.simple_tag(name='get')
def listaget(barmi, i):
    return barmi[i]


# @register.simple_tag(name='matrix')
# def matrix(pontmatrix, i, j):
#     return pontmatrix[int(i)][int(j)]


HIANYZO = '–'


def _szam_vagy_none(ertek):
    try:
        szam = float(ertek)
    except (TypeError, ValueError):
        return None
    return szam if math.isfinite(szam) else None


@register.simple_tag(name='ertekelesmezo')
def ertekelesmezo(ertekeloszotar, tanulo, mezo):
    """Egy tanuló értékelésének megjelenítendő szövege; hiányzó adat helyett '–'."""
    ertek = ertekeloszotar.get(tanulo, {}).get(mezo)
    if ertek is None or ertek == '-':
        return HIANYZO
    if mezo == 'szazalek':
        szam = _szam_vagy_none(ertek)
        return HIANYZO if szam is None else f'{round(szam * 100, 1):g}%'
    if mezo == 'pont':
        szam = _szam_vagy_none(ertek)
        return HIANYZO if szam is None else f'{round(szam, 2):g}'
    return ertek


@register.filter(name='statertek')
def statertek(ertek):
    """Statisztikai érték: a -1 (nincs adat), None és NaN helyett '–'."""
    szam = _szam_vagy_none(ertek)
    if szam is None or szam < 0:
        return HIANYZO
    return f'{round(szam, 2):g}'


@register.filter(name='szam')
def szam(ertek):
    szam = _szam_vagy_none(ertek)
    return HIANYZO if szam is None else f'{round(szam, 2):g}'
