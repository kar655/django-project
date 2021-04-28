from django import template

register = template.Library()


@register.filter
def dict_item(dictionary, position):
    return dictionary[position]
