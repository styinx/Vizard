import json
from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User, Task, TaskScheduler
from Vizard.settings import RESOURCE_PATH, RESPONSE
from Analyzer.models import Testplan, JMeter, Locust
from source.util import get_client_ip


scheduler = TaskScheduler()
scheduler_thread = Thread(target=scheduler.run)
scheduler_thread.daemon = True
scheduler_thread.start()


def index(request):
    return render(request, "Analyzer/Index.html")


def tasks(request):
    response = RESPONSE
    response["tasks"] = {}
    user = User(get_client_ip(request))

    for task in user.config["tasks"]:
        if user.valid(task):
            response["tasks"][task] = user.config["tasks"][task]["status"]

    return render(request, "Analyzer/Tasks.html", response)


def loadtest(request):
    return loadtest_jmeter(request)


def loadtest_jmeter(request):
    user = User(get_client_ip(request))
    task = Task(0)

    user.setTask(task)

    template = RESOURCE_PATH + "/JMeter_template.jmx"
    experiment = task.path + "/experiment.jmx"
    arguments = {
        "$DOMAIN": "www.example.com",
        "$THREADS": "10",
        "$DURATION": "2",
        "$RESULT_FILE": task.path + "/result.csv"}

    testplan = Testplan(template, experiment, arguments)

    jm = JMeter({
        "-n": "",
        "-t": testplan.target,
        "-L": "jmeter.util=WARN"
    })
    jm.arg_separator = " "

    task.setExecutionCallback(jm.execute, {"path": "/home/chris/Programme/apache-jmeter-4.0/bin/"})
    task.setProcessingCallback(jm.process)
    scheduler.addTask(task, user)

    conf = dict(jm.config)
    del conf["-t"]

    response = RESPONSE
    response["mail"] = user.mail
    response["tool"] = jm.name
    response["config"] = json.dumps(conf, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def loadtest_locust(request):
    user = User(get_client_ip(request))
    task = Task(0)

    user.setTask(task)

    lc = Locust({
        "-f":             RESOURCE_PATH + "Locust.py",
        "--csv":          user.hash + "/LC_" + task.hash,
        "--no-web":       "",
        "--only-summary": "",
        "-H":             "http://www.example.com",
        "-P":             "80",
        "-L":             "CRITICAL",
        "-c":             "10",
        "-t":             "2s",
        "-r":             "2"
    })
    lc.arg_separator = " "

    task.setExecutionCallback(lc.execute)
    task.setProcessingCallback(lc.process)
    scheduler.addTask(task, user)

    conf = dict(lc.config)
    del conf["--csv"]
    del conf["-f"]

    response = RESPONSE
    response["mail"] = user.mail
    response["tool"] = lc.name
    response["config"] = json.dumps(conf, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def stresstest(request):
    return HttpResponse("")
