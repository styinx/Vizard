from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User, Task, TaskScheduler
from Vizard.settings import RESPONSE
from Analyzer.execution import execute_jmeter, execute_locust
from source.util import dump

scheduler = TaskScheduler()
scheduler_thread = Thread(target=scheduler.run)
scheduler_thread.daemon = True
scheduler_thread.start()


def index(request):
    return render(request, 'Analyzer/Index.html')


def tasks(request, api=None):
    user = User(request)
    response = RESPONSE.copy()
    response['tasks'] = {}

    for task in user.get_tasks():
        if user.valid(task):
            response['tasks'][task] = user.config['tasks'][task]['status']

    return render(request, 'Analyzer/Tasks.html', response)


def loadtest(request, tool=None, api=None):
    response = RESPONSE.copy()

    if tool == "locust":
        response = execute_locust(request, response, scheduler)
    else:
        response = execute_jmeter(request, response, scheduler)

    if api:
        if "missing" not in response:
            scheduler.add_task_callback(response['hash'], request.GET['callback'])

        return HttpResponse(dump(response))

    return render(request, 'Analyzer/Analysis.html', response)


def stresstest(request, tool=None, api=None):
    response = RESPONSE.copy()

    return HttpResponse('TODO')
