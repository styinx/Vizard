from requests import Session

from django.template import Library
from Presenter.templatetags.text import *

register = Library()


@register.filter(name='wikipedia')
def wikipedia(page, args='400;True'):
    args = args.split(';')
    limit = int(args[0]) or 400
    link = bool(args[1]) or True
    api = 'https://en.wikipedia.org/w/api.php'
    wiki = 'https://en.wikipedia.org/wiki/' + page

    api = api + '?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=' + page
    result = Session().get(api).json()['query']['pages']
    text = result[list(result.keys())[0]]['extract']

    if link:
        reference = tag_value('[1]', 'sup;title="Taken from wikipedia.org"')
        return str(text[:text.find(' ', limit)] + '... '
                   + tag_value('continue reading' + reference, 'a;href="' + wiki + '" target="_"') + '.')
    else:
        return text[:text.find(' ', limit)] + '... '
