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
        text += str('Locust was used as the load testing tool.'
                    'During the execution of this experiment (' +
                    duration(meta['duration']) + ') ' +
                    important(args['load'] + ' virtual users') +
                    ' produced load to the tested domain (' +
                    important(args['domain'] + empty_text(args['port'])) + '). '
                    'The hatch rate of the users was ' +
                    s(int(args['hatch_rate']), ' user') + ' per second.')

    elif meta['tool'] == 'JMeter':
        text += str('JMeter was used as the load testing tool.'
                    'During the execution of this experiment (' +
                    duration(meta['duration']) + ') ' +
                    important(args['load'] + ' virtual users') +
                    ' produced load to the tested domain (' +
                    important(args['domain']) + '). ')

    return text + '<br>'


def experiment_tool_text(wiki):
    if wiki != '':
        return b('Tool description') + ':<br>' + wikipedia(wiki) + '<br>'
    return ''


def table_spline_text(values, meta):
    time_min = empty_text(better_duration(values['min']['ts'], meta['from']), 'after %s')
    time_max = empty_text(better_duration(values['max']['ts'], meta['from']), 'after %s')

    if time_min == '':
        time_min = 'at the beginning'
    if time_max == '':
        time_max = 'at the beginning'

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
               '  <td>' + time_min + '</td>'
               '  <td>' + time_max + '</td>'
               '  <td>-</td>'
               '  <td>-</td>'
               '</tr>'
               '<tr>'
               '  <td>Value:</td>'
               '  <td style="color: green">' + str(values['min']['val']) + ' ' + values['unit'] + '</td>'
               '  <td style="color: red">' + str(values['max']['val']) + ' ' + values['unit'] + '</td>'
               '  <td>' + str(values['mean']['val']) + ' ' + values['unit'] + '</td>'
               '  <td>' + str(values['p50']['val']) + ' ' + values['unit'] + '</td>'
               '</tr>'
               '</tbody>')


def table_gauge_text(values, meta):

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
               '  <td>' + '' + '</td>'
               '  <td>' + '' + '</td>'
               '  <td>-</td>'
               '  <td>-</td>'
               '</tr>'
               '<tr>'
               '  <td>Value:</td>'
               '  <td style="color: green">' + '' + '</td>'
               '  <td style="color: red">' + '' + '</td>'
               '  <td>' + '' + '</td>'
               '  <td>' + '' + '</td>'
               '</tr>'
               '</tbody>')


def explanation_text(definition):
    text = b('Info') + ':<br>'

    text += definition

    return text + '<br>'


def description_spline_text(values, meta):
    _from, _to = meta['from'], meta['to']
    _duration = _to - _from
    unit = values['unit']
    _max = values['max']
    _min = values['min']
    _max_text = str(_max['val']) + ' ' + unit
    _min_text = str(_min['val']) + ' ' + unit
    text = b('Summary') + ':<br>'

    choices_min_max = []
    choices_mean_percentile = []

    time_min = empty_text(better_duration(_min['ts'], _from), 'after %s')
    time_max = empty_text(better_duration(_max['ts'], _from), 'after %s')

    if time_min == '':
        time_min = 'at the beginning'
    if time_max == '':
        time_max = 'at the beginning'

    if values['min']['val'] != values['max']['val']:
        choices_min_max.append(str('The overall minimum was ' + important(_min_text) +
                                   ' (' + time_min + ')' +
                                   ' and the overall maximum was ' + important(_max_text) +
                                   ' (' + time_max + '). '))

        if values['max']['f'] != values['min']['f']:
            choices_min_max.append(str('The maximum of ' + _max_text +
                                       ' was recorded ' + important(times(_max['f'])) +
                                       ' while the minimum of ' + _min_text +
                                       ' was recorded ' + important(times(_min['f'])) + '.'))
        else:
            choices_min_max.append(str('The maximum of ' + _max_text +
                                       ' and the minimum of ' + _min_text + ' were recorded exactly ' +
                                       important(times(_min['f'])) + ' each.'))

    else:
        choices_min_max.append(str('The overall minimum of ' + important(_min_text) +
                                   ' was equal to the overall maximum and occurred ' +
                                   important(times(_min['f'])) + '.'))

    text += random_choices(choices_min_max, True)

    return text + '<br>'


def description_gauge_text(values, meta):
    text = b('Summary') + ':<br>'

    return text + '<br>'
