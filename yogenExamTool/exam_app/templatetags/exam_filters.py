import json
from django import template
register = template.Library()


@register.filter()
def times(min=5):
    return range(1, min+1)


@register.simple_tag
def define(val=None):
    my_dict = eval(val)
    return my_dict
