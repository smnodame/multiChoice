from django import template

register = template.Library()

@register.filter
def lower(value, arg):
    label = {
        '1': 'a',
        '2': 'b',
        '3': 'c',
        '4': 'd',
        '5': 'e'
    }
    return label[str(arg)]
