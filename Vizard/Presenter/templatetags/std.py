from django.template import Library
from Presenter.templatetags.text import *

register = Library()


@register.filter(name='dict_keys')
def dict_keys(d):
    return list(d.keys())
