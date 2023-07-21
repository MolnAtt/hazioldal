from django import template

register = template.Library()

@register.filter(name="szepszazalek")
def szepszazalek(x):
    try:
        return f'{round(float(x)*100)}%'
    except:
        return ''

jegy2class_szotar={
    '5*':'55',
    '5':'5',
    '4/5':'45',
    '4':'4',
    '3/4':'34',
    '3':'3',
    '2/3':'23',
    '2':'2',
    '1/2':'12',
    '1':'1',
    '-':'',
    '':'',
}
    
@register.filter(name="jegy2class")
def jegy2class(jegy):
    return jegy2class_szotar[jegy]
    