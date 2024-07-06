from django import template
from base.models import Group

register = template.Library()

@register.filter
def is_member(user, group_name):
    group = Group.objects.get(name=group_name)
    return group.members.filter(id=user.id).exists()
