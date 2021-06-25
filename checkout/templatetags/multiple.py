from django import template

register = template.Library()


def multiple(value, arg):
    return value * arg


register.filter('multiple', multiple)
