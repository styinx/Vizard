import re
from datetime import datetime as dt

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
        return text.replace('%s', val)
    else:
        return ""


@register.filter(name='date')
def date(ts, t_format='%d.%m %H:%M:%S'):
    return dt.utcfromtimestamp(ts / 1000).strftime(t_format)


@register.filter(name='duration')
def duration(ms, t_format='%Yy %dd %Hh %Mm %Ss %fms'):
    ms = int(ms) * 1000
    S = ms / 1000
    M = S / 60
    H = M / 60
    d = H / 24
    Y = d / 356

    if Y % 10 >= 1 and t_format.find('%Y') >= 0:
        t_format = t_format.replace('%Y', str(int(Y % 10)))
    else:
        t_format = t_format[t_format.find('%', 1):]

    if d % 356 >= 1 and t_format.find('%d') >= 0:
        t_format = t_format.replace('%d', str(int(d % 356)))
    else:
        t_format = re.sub('%d[^%]*%', '%', t_format)

    if H % 24 >= 1 and t_format.find('%H') >= 0:
        t_format = t_format.replace('%H', str(int(H % 24)))
    else:
        t_format = re.sub('%H[^%]*%', '%', t_format)

    if M % 60 >= 1 and t_format.find('%M') >= 0:
        t_format = t_format.replace('%M', str(int(M % 60)))
    else:
        t_format = re.sub('%M[^%]*%', '%', t_format)

    if S % 60 >= 1 and t_format.find('%S') >= 0:
        t_format = t_format.replace('%S', str(int(S % 60)))
    else:
        t_format = re.sub('%S[^%]*%', '%', t_format)

    if ms % 1000 >= 1 and t_format.find('%f') >= 0:
        t_format = t_format.replace('%f', str(int(ms % 1000)))
    else:
        t_format = re.sub('%f[^%]*', '', t_format)

    return t_format


@register.filter(name='idfy')
def idfy(text):
    return re.sub(r'\s', '_', text)


@register.filter(name='tag')
def tag(text, t):
    return '<' + t + '>' + text + '</' + t + '>'
