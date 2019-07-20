import re
from datetime import datetime as dt

from django.template import Library

register = Library()

NL = '\n'
BLK = ' '
NL_HT = '<br>'
BLK_HT = '&nbsp;'


@register.filter(name='keys')
def keys(d):
    return d.keys()


@register.filter(name='b')
def b(text):
    return tag(text, 'b')


@register.filter(name='i')
def i(text):
    return tag(text, 'i')


@register.filter(name='s')
def s(val, text):
    res = str(val) + text
    if abs(val) == 1:
        return res
    return res + 's'


@register.filter(name='important')
def important(text):
    return tag_value(text, 'span;class="important"')


@register.filter(name='times')
def times(val):
    if val == 0:
        return 'never'
    elif val == 1:
        return 'once'
    elif val == 2:
        return 'twice'
    return str(val) + ' times'


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
        else:
            return text

    elif isinstance(text, list):
        return [cap(x, which) if i == 0 else cap(x, 'None') for i, x in enumerate(text)]


@register.filter(name='empty_text')
def empty_text(val, text=''):
    if val != "":
        if text:
            return text.replace('%s', val)
        else:
            return val
    else:
        return ""


@register.filter(name='date')
def date(ts, t_format='%d.%m.%Y %H:%M:%S'):
    if t_format.find('%f') >= 0:
        return dt.utcfromtimestamp(ts / 1000).strftime(t_format)[:-4]
    return dt.utcfromtimestamp(ts / 1000).strftime(t_format)


@register.filter(name='better_date')
def better_date(ts, dur):
    __1m = 60000
    __1h = __1m * 60
    __1d = __1h * 24

    if dur < __1m:
        return date(ts, '%S.%f')
    elif dur < __1h:
        return date(ts, '%M:%S.%f')
    elif dur < __1d:
        return date(ts, '%H:%M:%S')
    else:
        return date(ts, '%d.%m %H:%M')


@register.filter(name='duration')
def duration(ms, t_format='%Y y %d d %H h %M m %S s %f ms'):
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


@register.filter(name='better_duration')
def better_duration(_to, _from):
    return duration(_to - _from)


@register.filter(name='idfy')
def idfy(text):
    return re.sub(r'\s', '_', text)


@register.filter(name='anchorfy')
def anchorfy(text, values):
    if isinstance(text, str):
        href, _id = values.split(';')
        return tag_value(text, 'a;href="#' + idfy(text) + href + '" id="' + idfy(text) + _id + '"')

    elif isinstance(text, list):
        return [anchorfy(x, values) for x in text]

    return ""


@register.filter(name='tag')
def tag(text, t):
    return '<' + t + '>' + text + '</' + t + '>'


@register.filter(name='tag_value')
def tag_value(text, values):
    t, values = values.split(';')
    return '<' + t + ' ' + values + '>' + text + '</' + t + '>'
