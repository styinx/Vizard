from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User, Task, TaskScheduler
from Vizard.settings import RESPONSE
from Analyzer.execution import execute_jmeter, execute_locust

scheduler = TaskScheduler()
scheduler_thread = Thread(target=scheduler.run)
scheduler_thread.daemon = True
scheduler_thread.start()


def index(request):
    return render(request, "Analyzer/Index.html")


def tasks(request):
    user = User(request)
    response = RESPONSE.copy()
    response["tasks"] = {}

    for task in user.getTasks():
        if user.valid(task):
            response["tasks"][task] = user.config["tasks"][task]["status"]

    return render(request, "Analyzer/Tasks.html", response)


def loadtest(request):
    return loadtest_jmeter(request)


def loadtest_jmeter(request):
    response = execute_jmeter(request, RESPONSE.copy(), scheduler)

    return render(request, "Analyzer/Analysis.html", response)


def loadtest_locust(request):
    response = execute_locust(request, RESPONSE.copy(), scheduler)

    return render(request, "Analyzer/Analysis.html", response)


def stresstest(request):
    return HttpResponse("TODO")
