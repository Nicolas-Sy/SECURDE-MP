from django.contrib.auth.models import Group
from django import template

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, BookManager):
    group =  Group.objects.get(name=BookManager) 
    return group in user.groups.all() 