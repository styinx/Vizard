from random import sample

from .templatetags.text import *
from .templatetags.util import *


def random_choices(text_list, strict=False):
    t = ''
    order = sample(range(0, len(text_list)), len(text_list))

    if strict:
        order = range(0, len(text_list))

    for index in order:
        t += text_list[index]

    return t


def experiment_summary_text(meta):
    d = meta['to'] - meta['from']
    text = b('Experiment summary') + ':<br>'
    text += str('From ' + date(meta['from']) + '  to ' + date(meta['to']) +
                ' ' + important(s(meta['samples'], ' value')) + ' were recorded. ')

    args = meta['arguments']

    if meta['tool'] == 'Locust':
        text += str('During the execution of this experiment (' +
                    duration(meta['duration']) + ') ' +
                    important(args['load'] + ' virtual users') +
                    ' produced load to the tested domain (' +
                    important(args['domain'] + empty_text(args['port'])) + '). '
                    'The hatch rate of the users was ' +
                    s(int(args['hatch_rate']), ' user') + ' per second.')

    elif meta['tool'] == 'JMeter':
        text += str('During the execution of this experiment (' +
                    duration(meta['duration']) + ') ' +
                    important(args['load'] + ' virtual users') +
                    ' produced load to the tested domain (' +
                    important(args['domain']) + '). '
                    '')

    return text + '<br>'


def experiment_tool_text(wiki):
    if wiki != '':
        return b('Tool description') + ':<br>' + wikipedia(wiki) + '<br>'
    return ''


def table_text(values, meta):
    return str('<thead class="thead">'
               '<tr>'
               '  <th scope="col"></th>'
               '  <th scope="col">Min.</th>'
               '  <th scope="col">Max.</th>'
               '  <th scope="col">Mean.</th>'
               '  <th scope="col">Med.</th>'
               '</tr>'
               '</thead>'
               '<tbody>'
               '<tr>'
               '  <td>Time:</td>'
               '  <td>after ' + better_duration(values['min'][0], meta['from']) + '</td>'
               '  <td>after ' + better_duration(values['max'][0], meta['from']) + '</td>'
               '  <td>-</td>'
               '  <td>-</td>'
               '</tr>'
               '<tr>'
               '  <td>Value:</td>'
               '  <td style="color: green">' + str(values['min'][1]) + ' ' + values['unit'] + '</td>'
               '  <td style="color: red">' + str(values['max'][1]) + ' ' + values['unit'] + '</td>'
               '  <td>' + str(values['mean']) + ' ' + values['unit'] + '</td>'
               '  <td>' + str(values['med']) + ' ' + values['unit'] + '</td>'
               '</tr>'
               '</tbody>')


def explanation_text(definition):
    text = b('Info') + ':<br>'

    text += definition

    return text + '<br>'


def description_text(values, meta):
    _from, _to = meta['from'], meta['to']
    _duration = _to - _from
    unit = values['unit']
    _max = str(values['max'][1]) + ' ' + unit
    _min = str(values['min'][1]) + ' ' + unit
    text = b('Summary') + ':<br>'

    choices_min_max = []
    choices_mean_med = []

    if values['min'][1] != values['max'][1]:
        choices_min_max.append(str('The overall minimum was ' + important(_min) +
                                   ' (after ' + better_duration(values['min'][0], _from) + ')' +
                                   ' and the overall maximum was ' + important(_max) +
                                   ' (' + better_duration(values['max'][0], _from) + '). '))

        if values['max_frequency'] != values['min_frequency']:
            choices_min_max.append(str('The maximum of ' + _max +
                                       ' was recorded ' + important(times(values['max_frequency'])) +
                                       ' while the minimum of ' + _min +
                                       ' was recorded ' + important(times(values['min_frequency'])) + '.'))
        else:
            choices_min_max.append(str('The maximum of ' + _max + ' and the minimum of ' + _min +
                                       ' were recorded exactly ' +
                                       important(times(values['min_frequency'])) + ' each.'))

    else:
        choices_min_max.append(str('The overall minimum of ' + important(_min) +
                                   ' was equal to the overall maximum and occurred ' +
                                   important(times(values['min_frequency'])) + '.'))

    text += random_choices(choices_min_max, True)

    return text + '<br>'
