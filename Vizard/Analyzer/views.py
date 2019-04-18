import json
from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User, Task, TaskScheduler
from Vizard.settings import RESOURCE_PATH, RESPONSE
from Analyzer.models import Testplan, JMeter, Locust, Vizardplan

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
    user = User(request)
    task = Task(0)
    user.setTask(task, path=task.hash)

    result_file = task.path + "/result.csv"
    experiment_file = task.path + "/experiment.jmx"
    arguments = {
        "$DOMAIN":      "www.example.com",
        "$THREADS":     "10",
        "$DURATION":    "2",
        "$RESULT_FILE": result_file}

    configuration = {
        "tool":       "JMeter",
        "experiment": experiment_file,
        "task":       task.hash,
        "arguments":  arguments
    }

    Vizardplan(task.path + "/vizard.json", configuration)
    testplan = Testplan(RESOURCE_PATH + "/JMeter_template.jmx", experiment_file, arguments)

    jm = JMeter({
        "-n": "",
        "-t": testplan.target,
        "-L": "jmeter.util=WARN"
    })
    jm.arg_separator = " "

    task.setExecutionCallback(jm.execute, {"path": "/home/chris/Programme/apache-jmeter-5.1.1/bin/"})
    task.setProcessingCallback(jm.process, {"path": result_file})
    scheduler.addTask(task, user)

    conf = dict(jm.config)
    del conf["-t"]

    response = RESPONSE.copy()
    response["mail"] = user.mail
    response["tool"] = jm.name
    response["config"] = json.dumps(conf, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def loadtest_locust(request):
    user = User(request)
    task = Task(0)
    user.setTask(task, path=task.hash)

    experiment_file = task.path + "/experiment.py"
    arguments = {
        "$MIN_WAIT":    "1000",
        "$MAX_WAIT":    "2000",
        "$RESULT_FILE": task.path + "/result_processed.json"}

    configuration = {
        "tool":       "Locust",
        "experiment": experiment_file,
        "task":       task.hash,
        "arguments":  arguments
    }

    Vizardplan(task.path + "/vizard.json", configuration)
    testplan = Testplan(RESOURCE_PATH + "/Locust_template.py", experiment_file, arguments)

    lc = Locust({
        "-f":             testplan.target,
        "--csv":          task.path + "/",
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
    scheduler.addTask(task, user)

    conf = dict(lc.config)
    del conf["--csv"]
    del conf["-f"]

    response = RESPONSE.copy()
    response["mail"] = user.mail
    response["tool"] = lc.name
    response["config"] = json.dumps(conf, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def stresstest(request):
    return HttpResponse("")
