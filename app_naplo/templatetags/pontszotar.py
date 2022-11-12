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
    return "kulcshiba"

@register.simple_tag(name='listaget')
def listaget(lista, i):
    return lista[i]



# @register.simple_tag(name='matrix')
# def matrix(pontmatrix, i, j):
#     return pontmatrix[int(i)][int(j)]