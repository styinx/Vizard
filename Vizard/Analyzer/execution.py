import re

from source.util import unpack_request_values, dump

from Vizard.settings import CONF_JMETER, CONF_LOCUST
from Vizard.models import User, Task

from Analyzer.tools import *


# Sets default test values.
# Fields with the value 'None' are mandatory.
def unpack_jmeter_values(request):
    return unpack_request_values(request, {
        'domain':     None,
        'port':       '',
        'duration':   '10',
        'load':       '10',

        # jmeter
        'ramp_up':    '1',
        'ramp_down':  '1',
    })


def unpack_locust_values(request):
    return unpack_request_values(request, {
        'domain':     None,
        'port':       '',
        'duration':   '10',
        'load':       '10',

        # locust
        'min_wait':   '1000',
        'max_wait':   '2000',
        'hatch_rate': '1'
    })


def execute_jmeter(request, response, scheduler):
    task = Task(0)
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
    task = Task(0)
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
