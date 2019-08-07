from django.template import Library
from Presenter.templatetags.text import *

register = Library()


@register.filter(name='dict_keys')
def dict_keys(d):
    return list(d.keys())


@register.filter(name='dict_elem')
def dict_elem(d, key):
    return d[key]
