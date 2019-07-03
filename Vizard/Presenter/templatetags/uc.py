import re
from datetime import datetime as dt

from django.template import Library
from Presenter.templatetags.text import *

register = Library()

QUERIES = [
    'What was the $metric|select|uc-metric of the domain $domain|text between $start|datetime and $stop|datetime.'
]


@register.filter(name='query')
def query(choice, values):
    text = QUERIES[choice]

    while re.match(r'\$([a-z]+)\|([a-z]+)\|([a-z]+)', text):
        text = re.sub()

    return tag(text, 'p')
