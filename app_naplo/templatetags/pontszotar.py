from django import template

register = template.Library()

@register.simple_tag(name='getget')
def getget(pontszotar, tanulo, feladat):
    return pontszotar[tanulo][feladat]

# @register.simple_tag(name='matrix')
# def matrix(pontmatrix, i, j):
#     return pontmatrix[int(i)][int(j)]