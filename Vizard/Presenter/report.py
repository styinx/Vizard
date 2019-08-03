import os
import json
from time import strftime, gmtime

from django.template.loader import render_to_string

from Presenter.report_text import explanation_text, description_spline_text, experiment_summary_text, \
    experiment_tool_text, \
    table_spline_text, table_gauge_text, description_gauge_text
from source.util import dump, write, read, pack_zip_files, unserialize

from Vizard.settings import TASK_PATH, STATIC_URL, BASE_DIR, DATE_FORMAT, REPORT, VALUES
from Vizard.models import User


class Report:
    def __init__(self, request, response, api, _id, export):
        self.request = request
        self.response = response
        self.api = api
        self._id = _id if _id is not None else ''
        self.path = TASK_PATH + '/' + self._id
        self.export = export

        self.data_template = 'Data.html'
        self.report_template = 'Report.html'

    def collect_data(self):
        raise NotImplementedError

    def collect_report(self):
        raise NotImplementedError

    def collect_report_result(self):
        raise NotImplementedError

    def export_report(self):
        raise NotImplementedError


class ReportFactory:
    @staticmethod
    def create_instance(request, response, api, _id, export):
        # meta = read(TASK_PATH + '/' + _id + '/vizard.json')
        #
        # if meta['type'] == 'loadtest':
        #     return LoadtestReport(request, response, api, _id, export)
        #
        # elif meta['type'] == 'regressiontest':
        #     return RegressionTest(request, response, api, _id, export)

        return LoadtestReport(request, response, api, _id, export)


class LoadtestReport(Report):
    def __init__(self, request, response, api, _id, export):
        super().__init__(request, response, api, _id, export)

        self.data_template = 'LoadtestData.html'
        self.report_template = 'LoadtestReport.html'

    def collect_data(self):
        user = User(self.request)

        if self.api:
            self.response['experiments'] = {}
            tasks_info = user.get_tasks()

            # TODO run only necessary tasks
            for experiment in tasks_info:
                self.response['experiments'][experiment] = read(TASK_PATH + '/' + experiment + '/result_processed.json')

            if self._id:
                return str(self.response['experiments'][self._id])

            return str(self.response['experiments'])

        if self._id:
            if user.valid(self._id):
                data = json.loads(read(TASK_PATH + '/' + self._id + '/result_processed.json'))

                self.response['task'] = self._id
                self.response['data'] = dump(data)
                return self.response

            self.response['status'] = '404'
            self.response['message'] = str('Sorry, the requested job id (' + str(self._id) +
                                           ') seems not to exists or is not ready yet.')

            return self.response

        self.response['experiments'] = {}

        tasks_info = user.get_tasks()
        for experiment in tasks_info:
            started = strftime(DATE_FORMAT, gmtime(tasks_info[experiment]['started']))
            completed = strftime(DATE_FORMAT, gmtime(tasks_info[experiment]['completed']))
            self.response['experiments'][experiment] = {'started': started, 'completed': completed}

        return self.response

    def collect_report(self):
        User(self.request)

        self.response['hash'] = self._id
        self.response['metrics'] = {}

        try:
            path = TASK_PATH + '/' + self._id
            df = unserialize(path + '/result_cached.dat').df
            meta = read(path + '/vizard.json')

            self.response['meta'] = {
                'tool':      meta['tool'],
                'tool_wiki': REPORT[meta['tool']]['wiki'],
                'tool_link': REPORT[meta['tool']]['link'],
                'samples':   df.shape[0],
                'from':      df.index[0],
                'to':        df.index[len(df.index) - 1],
                'duration':  df.index[len(df.index) - 1] - df.index[0],
                'arguments': meta['arguments']
            }

            self.response['meta']['text'] = {
                'experiment': experiment_summary_text(self.response['meta']),
                'wiki':       experiment_tool_text(REPORT[meta['tool']]['wiki'])
            }

            metrics = REPORT[meta['tool']]['metrics']
            for metric in metrics:
                unit = metrics[metric]['unit']
                chart_type = metrics[metric]['type']
                index = metrics[metric]['col']

                if isinstance(index, list):
                    df['temp'] = df[index].sum(axis=1)
                    index = 'temp'

                _frequency = df[index].value_counts().to_dict()
                _min = df[index].min()
                _max = df[index].max()
                _mean = df[index].mean()
                _p5 = df[index].quantile(0.05, interpolation='nearest')
                _p25 = df[index].quantile(0.25, interpolation='nearest')
                _p50 = df[index].quantile(0.50, interpolation='nearest')
                _p75 = df[index].quantile(0.75, interpolation='nearest')
                _p95 = df[index].quantile(0.95, interpolation='nearest')
                _samples = int(self.response['meta']['samples'])
                _from = self.response['meta']['from']
                _to = self.response['meta']['to']

                self.response['metrics'][metric] = {
                    'unit': unit,
                    'type': chart_type
                }

                if chart_type == 'gauge':
                    _sum = sum(_frequency.values())
                    self.response['metrics'][metric].update({
                        'data': [{'name':        str(round((val / _sum) * 100, 2)) + '%<br>' + VALUES[str(key)],
                                  'description': VALUES[str(key)],
                                  'y':           round((val / _sum) * 100, 2),
                                  'abs':         val,
                                  'sum':         _sum
                                  } for key, val in _frequency.items()]
                    })

                    self.response['metrics'][metric]['text'] = {
                        'table':       table_gauge_text(None, None),
                        'explanation': explanation_text(metrics[metric]['definition']),
                        'description': description_gauge_text(None, None)
                    }

                else:
                    data = [[x[0], round(x[1], 2)] for x in df[index].items()]
                    if len(_frequency) > 5:
                        cumulative = [[round(x, 2), round((i + 1) / _samples * 100)] for i, x in enumerate(sorted(df[index].values))]
                    else:
                        cumulative = []

                    self.response['metrics'][metric].update({
                        'data':        data,
                        'cumulative':  cumulative,
                        'min':         {'ts': df[index].idxmin(), 'val': round(_min, 2), 'f': _frequency[_min]},
                        'max':         {'ts': df[index].idxmax(), 'val': round(_max, 2), 'f': _frequency[_max]},
                        'mean':        {'val': round(_mean, 2)},
                        'p5':          {'val': round(_p5, 2), 'f': round(_frequency[_p5], 2)},
                        'p25':         {'val': round(_p25, 2), 'f': round(_frequency[_p25], 2)},
                        'p50':         {'val': round(_p50, 2), 'f': round(_frequency[_p50], 2)},
                        'p75':         {'val': round(_p75, 2), 'f': round(_frequency[_p75], 2)},
                        'p95':         {'val': round(_p95, 2), 'f': round(_frequency[_p95], 2)},
                        'total':       round(df[index].sum(), 2),
                        'from':        _from,
                        'to':          _to,
                        'frequencies': {k: round(_frequency[k], 2) for k in list(_frequency)[:3]}
                    })

                    print(self.response['metrics'][metric])

                    self.response['metrics'][metric]['text'] = {
                        'table':       table_spline_text(self.response['metrics'][metric], self.response['meta']),
                        'explanation': explanation_text(metrics[metric]['definition']),
                        'description': description_spline_text(self.response['metrics'][metric], self.response['meta'])
                    }

            if self.export is None:
                return self.response, None

            else:
                return self.response, self.export_report()

        except FileNotFoundError:
            self.response['status'] = '404'
            self.response['message'] = 'Sorry, the requested id (' + str(self._id) + ') seems not to exists.'
            return self.response, None

    def collect_report_result(self):
        user = User(self.request)

        if self._id in user.get_tasks():
            task = user.get_tasks()[self._id]
            path = TASK_PATH + '/' + task['path']
            config = read(path + '/vizard.json')

            return str(config)

        return self.response

    def export_report(self):
        static_url = BASE_DIR + STATIC_URL

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
            self.path + '/Report.html':                  'Report.html'
        }

        html_content = render_to_string('Presenter/LoadtestReport.html', self.response).replace('/static/', './static/')
        write(html_content, self.path + '/Report.html')

        return self._id + '.zip', pack_zip_files(files_to_zip, self._id)


class CompareReport(Report):
    def __init__(self, request, response, api, id1, id2, export):
        super().__init__(request, response, api, id1 + '-' + id2, export)

        self.id1 = id1
        self.id2 = id2

        self.data_template = 'CompareData.html'
        self.report_template = 'CompareReport.html'

    def collect_data(self):
        pass

    def collect_report(self):
        User(self.request)

        self.response['hash1'] = self.id1
        self.response['hash2'] = self.id2
        self.response['metrics'] = {}

        try:
            path = TASK_PATH + '/' + self.id1
            df = unserialize(path + '/result_cached.dat').df
            meta = read(path + '/vizard.json')

            self.response['meta'] = {
                'tool':      meta['tool'],
                'tool_wiki': REPORT[meta['tool']]['wiki'],
                'tool_link': REPORT[meta['tool']]['link'],
                'samples':   df.shape[0],
                'from':      df.index[0],
                'to':        df.index[len(df.index) - 1],
                'duration':  df.index[len(df.index) - 1] - df.index[0],
                'arguments': meta['arguments']
            }

            metrics = REPORT[meta['tool']]['metrics']
            for metric in metrics:
                unit = metrics[metric]['unit']
                chart_type = metrics[metric]['type']
                index = metrics[metric]['col']

                if isinstance(index, list):
                    df['temp'] = df[index].sum(axis=1)
                    index = 'temp'

                self.response['metrics'][metric] = {
                    'unit':   unit,
                    'type':   chart_type,
                    'series': []
                }

                if chart_type == 'gauge':
                    pass
                else:
                    start = df.index[0]
                    data = [[x[0] - start, round(x[1], 2)] for x in df[index].items()]
                    self.response['metrics'][metric]['series'].append(data)

            path = TASK_PATH + '/' + self.id2
            df = unserialize(path + '/result_cached.dat').df
            meta = read(path + '/vizard.json')

            metrics = REPORT[meta['tool']]['metrics']
            for metric in metrics:

                if metric in self.response['metrics']:
                    chart_type = metrics[metric]['type']
                    index = metrics[metric]['col']

                    if isinstance(index, list):
                        df['temp'] = df[index].sum(axis=1)
                        index = 'temp'

                    if chart_type == 'gauge':
                        pass
                    else:
                        start = df.index[0]
                        data = [[x[0] - start, round(x[1], 2)] for x in df[index].items()]
                        self.response['metrics'][metric]['series'].append(data)

            if self.export is None:
                return self.response, None

            else:
                return self.response, self.export_report()

        except FileNotFoundError:
            self.response['status'] = '404'
            self.response['message'] = 'Sorry, the requested id (' + str(self._id) + ') seems not to exists.'
            return self.response, None

    def collect_report_result(self):
        user = User(self.request)

        id1, id2 = self._id.split('-')
        config = ''

        if id1 in user.get_tasks():
            task = user.get_tasks()[id1]
            path = TASK_PATH + '/' + task['path']
            config += str(read(path + '/vizard.json'))

        if id2 in user.get_tasks():
            task = user.get_tasks()[id2]
            path = TASK_PATH + '/' + task['path']
            config += str(read(path + '/vizard.json'))

        if config != '':
            return config

        return self.response

    def export_report(self):

        static_url = BASE_DIR + STATIC_URL

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
            self.path + '/Report.html':                  'Report.html'
        }

        if not os.path.isfile(self.path):
            os.makedirs(self.path)

        html_content = render_to_string('Presenter/CompareReport.html', self.response).replace('/static/', './static/')
        write(html_content, self.path + '/Report.html')

        return self._id + '.zip', pack_zip_files(files_to_zip, self._id)
