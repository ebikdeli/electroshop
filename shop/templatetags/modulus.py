from django import template

register = template.Library()


@register.filter(name='modulus')
def modulus(value, arg):
    if not value % arg:
        return True
    else:
        return False
