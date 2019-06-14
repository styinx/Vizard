import re
from django.template import Library

register = Library()


@register.filter(name='s')
def s(val, text):
    res = str(val) + text
    if abs(val) == 1:
        return res
    return res + 's'


@register.filter(name='idx')
def idx(val):
    if val % 10 == 1:
        return str(val) + 'st'
    elif val % 10 == 2:
        return str(val) + 'nd'
    elif val % 10 == 3:
        return str(val) + 'rd'
    else:
        return str(val) + 'th'


@register.filter(name='cap')
def cap(text, which='first'):
    if isinstance(text, str):
        if which == 'first':
            return text[0].upper() + text[1:]
        elif which == 'all':
            return ' '.join([cap(x) for x in text.split(' ')])

    return text


@register.filter(name='empty')
def empty(val, text):
    if val != "":
        return text
    else:
        return ""


@register.filter(name='idfy')
def idfy(text):
    return re.sub(r'\s', '_', text)


@register.filter(name='tag')
def tag(text, t):
    return '<' + t + '>' + text + '</' + t + '>'
