import datetime as dt

from source.util import unpack_request_values

from Vizard.settings import CONF_JMETER, CONF_LOCUST, RESPONSE
from Vizard.models import User, Task

from Analyzer.tools import *

d_jmeter = {
    'metric':    None,
    'domain':    None,
    'port':      '',
    'duration':  '10',
    'load':      '10',

    # jmeter
    'ramp_up':   '1',
    'ramp_down': '1',
}

d_locust = {
    'metric':     None,
    'domain':     None,
    'port':       '',
    'duration':   '10',
    'load':       '10',

    # locust
    'min_wait':   '1000',
    'max_wait':   '2000',
    'hatch_rate': '1'
}

d_regression = {
    'metric':        None,
    'domain':        None,
    'domain_first':  '',
    'domain_second': '',
    'start_first':   None,
    'start_second':  None
}


# Sets default test values.
# Fields with the value 'None' are mandatory.
def unpack_jmeter_values(request):
    return unpack_request_values(request, d_jmeter)


def unpack_locust_values(request):
    return unpack_request_values(request, d_locust)


def unpack_regression_values(request):
    return unpack_request_values(request, d_regression)


def execute_jmeter(request, response, scheduler):
    delay = 0

    if 'delay' in request.GET:
        delay = request.GET['delay']

    task = Task(delay)
    user = User(request)

    values = unpack_jmeter_values(request)

    if isinstance(values, list):
        response['missing'] = values
        return response

    user.set_task(task, path=task.hash)
    task.create_path()

    result_file = task.path + '/result.csv'
    loadtest_arguments = {
        '$DOMAIN':      values['domain'],
        '$THREADS':     values['load'],
        '$DURATION':    values['duration'],
        '$RESULT_FILE': result_file}

    vizard_configuration = {
        'tool':      'JMeter',
        'task':      task.hash,
        'arguments': values
    }

    Vizardplan(task, vizard_configuration)
    testplan = Testplan(CONF_JMETER['template'],
                        task.path + '/experiment.jmx',
                        loadtest_arguments)

    jm = JMeter({
        '-n': '',
        '-t': testplan.target,
        '-L': 'jmeter.util=WARN'
    })
    jm.arg_separator = ' '

    task.set_execution_callback(jm.execute, {'path': CONF_JMETER['executable_path']})
    task.set_processing_callback(jm.process, {'path': result_file})
    scheduler.add_task(task, user)

    conf = dict(jm.config)
    del conf['-t']

    response['tool'] = jm.name
    response['config'] = dump(conf)
    response['hash'] = task.hash

    return response


def execute_locust(request, response, scheduler):
    delay = 0

    if 'delay' in request.GET:
        delay = request.GET['delay']

    task = Task(delay)
    user = User(request)

    values = unpack_locust_values(request)

    if isinstance(values, list):
        response['missing'] = values
        return response

    if not values['domain'].startswith('http'):
        values['domain'] = 'http://' + values['domain']

    user.set_task(task, path=task.hash)
    task.create_path()

    result_file = task.path + '/result.csv'

    loadtest_arguments = {
        '$MIN_WAIT':    values['min_wait'],
        '$MAX_WAIT':    values['max_wait'],
        '$RESULT_FILE': result_file}

    vizard_configuration = {
        'tool':      'Locust',
        'task':      task.hash,
        'arguments': values
    }

    Vizardplan(task, vizard_configuration)
    testplan = Testplan(CONF_LOCUST['template'],
                        task.path + '/experiment.py',
                        loadtest_arguments)

    lc = Locust({
        '-f':             testplan.target,
        '--csv':          task.path + '/',
        '--no-web':       '',
        '--only-summary': '',
        '-H':             values['domain'],
        # '-P':             values['port'],
        # '-L':             'CRITICAL',
        '-c':             values['load'],
        '-t':             values['duration'] + 's',
        '-r':             values['hatch_rate']
    })
    lc.arg_separator = ' '

    task.set_execution_callback(lc.execute)
    task.set_processing_callback(lc.process, {'path': result_file})
    scheduler.add_task(task, user)

    conf = dict(lc.config)
    del conf['--csv']
    del conf['-f']

    response['tool'] = lc.name
    response['config'] = dump(conf)
    response['hash'] = task.hash

    return response


def execute_regressiontest(request, response, tool, scheduler):
    values = unpack_regression_values(request)

    if isinstance(values, list):
        response['missing'] = values
        return response

    request.GET._mutable = True

    response1 = RESPONSE.copy()
    request1 = request
    response2 = RESPONSE.copy()
    request2 = request

    request1.GET._mutable = True
    request2.GET._mutable = True

    request1.GET['metric'] = values['metric']
    request2.GET['metric'] = values['metric']

    if 'start_first' in values and 'start_second' in values:
        now = dt.datetime.now()
        d1 = dt.datetime.strptime(values['start_first'], '%d-%m-%Y|%H:%M:%S')
        d2 = dt.datetime.strptime(values['start_second'], '%d-%m-%Y|%H:%M:%S')

        if d1 > now and d2 > now:
            request1.GET['delay'] = (d1 - now).total_seconds()
            request2.GET['delay'] = (d2 - now).total_seconds()
        else:
            response['error'] = 'One or both starting times lie in the past.'

    elif 'domain_first' in values and 'domain_second' in values:
        request1.GET['domain'] = values['domain_first']
        request2.GET['domain'] = values['domain_second']

    if tool == 'Locust':
        response1 = execute_locust(request1, response1, scheduler)
        response2 = execute_locust(request2, response2, scheduler)
    else:
        response1 = execute_jmeter(request1, response1, scheduler)
        response2 = execute_jmeter(request2, response2, scheduler)

    if "missing" in response1 or 'missing' in response2:
        response['error'] = 'Something went wrong executing your tests.'
    else:
        response['tool'] = response1['tool']
        response['config'] = response1['config']
        response['hash1'] = response1['hash']
        response['hash2'] = response2['hash']

    return response
