from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return group_name in [ gn[0] for gn in user.groups.values_list('name')]