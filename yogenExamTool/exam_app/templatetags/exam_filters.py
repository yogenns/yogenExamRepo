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


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def contain(val_list, key):
    return key in val_list


@register.filter
def correct_or_wrong(answered_list, correct_list):
    correct_list = eval(correct_list)
    answered_list.sort()
    correct_list.sort()
    if answered_list == correct_list:
        return "Correct"
    else:
        return "Wrong"
