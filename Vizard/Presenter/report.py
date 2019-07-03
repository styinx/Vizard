import json
from time import strftime, gmtime

from django.template.loader import render_to_string

from Presenter.report_text import explanation_text, description_text, experiment_summary_text, experiment_tool_text, \
    table_text
from source.util import dump, write, read, pack_zip_files, unserialize

from Vizard.settings import TASK_PATH, STATIC_URL, BASE_DIR, DATE_FORMAT, REPORT
from Vizard.models import User


def collect_data(request, response, api, _id):
    user = User(request)

    if api:
        response['experiments'] = {}
        tasks_info = user.get_tasks()

        # TODO run only necessary tasks
        for experiment in tasks_info:
            response['experiments'][experiment] = read(TASK_PATH + '/' + experiment + '/result_processed.json')

        if _id:
            return str(response['experiments'][_id])

        return str(response['experiments'])

    if _id:
        if user.valid(_id):
            data = json.loads(read(TASK_PATH + '/' + _id + '/result_processed.json'))

            response['task'] = _id
            response['data'] = dump(data)
            return response

        response['status'] = '404'
        response['message'] = 'Sorry, the requested job id (' + str(_id) + ') seems not to exists.'

        return response

    response['experiments'] = {}

    tasks_info = user.get_tasks()
    for experiment in tasks_info:
        started = strftime(DATE_FORMAT, gmtime(tasks_info[experiment]['started']))
        completed = strftime(DATE_FORMAT, gmtime(tasks_info[experiment]['completed']))
        response['experiments'][experiment] = {'started': started, 'completed': completed}

    return response


def collect_report(request, response, _id, export):
    user = User(request)

    response['hash'] = _id
    response['metrics'] = {}

    try:
        path = TASK_PATH + '/' + _id
        df = unserialize(path + '/result_cached.dat').df
        meta = read(path + '/vizard.json')

        response['meta'] = {
            'tool':      meta['tool'],
            'tool_wiki': REPORT[meta['tool']]['wiki'],
            'tool_link': REPORT[meta['tool']]['link'],
            'samples':   df.shape[0],
            'from':      df.index[0],
            'to':        df.index[len(df.index) - 1],
            'duration':  df.index[len(df.index) - 1] - df.index[0],
            'arguments': meta['arguments']
        }

        response['meta']['text'] = {
            'experiment': experiment_summary_text(response['meta']),
            'wiki':       experiment_tool_text(REPORT[meta['tool']]['wiki'])
        }

        metrics = REPORT[meta['tool']]['metrics']
        for metric in metrics:
            unit = metrics[metric]['unit']
            chart_type = metrics[metric]['type']
            index = metrics[metric]['col']

            frequency = df[index].value_counts().to_dict()
            _min = df[index].min()
            _max = df[index].max()

            response['metrics'][metric] = {
                'unit':          unit,
                'type':          chart_type,
                'data':          [[x[0], x[1]] for x in df[index].items()],
                'cumulative':    sorted(df[index].values),
                'min':           [df[index].idxmin(), round(_min, 2)],
                'max':           [df[index].idxmax(), round(_max, 2)],
                'mean':          round(df[index].mean(), 2),
                'med':           round(df[index].median(), 2),
                'total':         round(df[index].sum(), 2),
                'frequencies':   {k: frequency[k] for k in list(frequency)[:3]},
                'min_frequency': frequency[_min],
                'max_frequency': frequency[_max],
            }

            response['metrics'][metric]['text'] = {
                'table': table_text(response['metrics'][metric], response['meta']),
                'explanation': explanation_text(metrics[metric]['definition']),
                'description': description_text(response['metrics'][metric], response['meta'])
            }

        if export is None:
            return response, None

        else:
            return response, export_report(response, path, _id)

    except FileNotFoundError:
        response['status'] = '404'
        response['message'] = 'Sorry, the requested id (' + str(_id) + ') seems not to exists.'
        return response, None


def collect_report_result(request, response, _id):
    user = User(request)

    if _id in user.get_tasks():
        task = user.get_tasks()[_id]
        path = TASK_PATH + '/' + task['path']
        config = read(path + '/vizard.json')

        return str(config)

    return response


def export_report(response, path, _id):
    static_url = BASE_DIR + '/' + STATIC_URL

    files_to_zip = {
        static_url + 'css/bootstrap.min.css':        'static/css/bootstrap.min.css',
        static_url + 'css/main.css':                 'static/css/main.css',
        static_url + 'css/report.css':               'static/css/report.css',
        static_url + 'js/bootstrap.min.js':          'static/js/bootstrap.min.js',
        static_url + 'js/jquery.min.js':             'static/js/jquery.min.js',
        static_url + 'js/highstock.js':              'static/js/highstock.js',
        static_url + 'js/charts.js':                 'static/js/charts.js',
        static_url + 'js/util.js':                   'static/js/util.js',
        static_url + 'js/text.js':                   'static/js/text.js',
        static_url + 'img/query_note.png':           'static/img/query_note.png',
        static_url + 'img/download.svg':             'static/img/download.svg',
        static_url + 'img/settings_transparent.svg': 'static/img/settings_transparent.svg',
        path + '/Report.html':                       'Report.html'
    }

    html_content = render_to_string('Presenter/Report.html', response).replace('/static/', './static/')
    write(html_content, path + '/Report.html')

    return _id + '.zip', pack_zip_files(files_to_zip, _id)
