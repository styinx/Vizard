from time import time
import json

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User
from source.analyze import JMeter, Locust
from source.scheduler import Task, TaskScheduler
from source.util import get_client_ip


ANALYSIS_PATH = "Vizard/resource/"
ANALYSIS_TESTS_PATH = "Vizard/resource/tests"
RESPONSE = {
    "status": 200,
    "message": ""
}


def index(request):
    return render(request, "Analyzer/Index.html")


def loadtest(request):
    return loadtest_jmeter(request)


def loadtest_jmeter(request):

    user = User(get_client_ip(request))

    jm = JMeter({
        "-n": "",
        "-t": ANALYSIS_PATH + "JMeter.jmx",
        "-l": user.hash + "/JM_" + str(time()) + ".csv",
        "-L": "jmeter.util=WARN"
    })
    jm.arg_separator = " "

    task = Task(jm.execute, 0, ("path",), ("/home/chris/Programme/apache-jmeter-4.0/bin/",))
    scheduler = TaskScheduler()
    scheduler.add(task)

    response = RESPONSE
    response["mail"] = user.mail
    response["tool"] = jm.name
    response["config"] = json.dumps(jm.config, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def loadtest_locust(request):
    lc = Locust({
        "-f":             ANALYSIS_PATH + "Locust.py",
        "--csv":          ANALYSIS_TESTS_PATH + get_client_ip(request) + "/JM_" + str(time()),
        "--no-web":       "",
        "--only-summary": "",
        "-H":             "www.example.com",
        "-P":             "80",
        "-L":             "CRITICAL",
        "-c":             "10",
        "-t":             "2s",
        "-r":             "2"
    })
    lc.arg_separator = " "

    task = Task(lc.execute, 0)
    scheduler = TaskScheduler()
    scheduler.add(task)

    return HttpResponse("loadtest (" + task.hash + ") with Locust is running")


def stresstest(request):
    return HttpResponse("")
