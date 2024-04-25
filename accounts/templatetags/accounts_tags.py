from django import template
from django.shortcuts import get_object_or_404
from accounts.models import *
register = template.Library()


@register.filter
def get_last_movement(pk):
    user = get_object_or_404(CustomUser, id=pk)
    timing = TimeManagement.objects.filter(user=user).last()
    return timing
