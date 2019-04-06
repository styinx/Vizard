from threading import Thread
import json
import os
import pickle

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User
from Vizard.settings import ANALYSIS_PATH, RESPONSE

from source.analyze import JMeter, Locust
from source.scheduler import Task, TaskScheduler
from source.util import get_client_ip


scheduler = TaskScheduler()
scheduler_thread = Thread(target=scheduler.run)
scheduler_thread.daemon = True
scheduler_thread.start()


def index(request):
    return render(request, "Analyzer/Index.html")


def jobs(request):
    response = RESPONSE
    jobs = {}

    if os.path.exists("tasks.dat"):
        jobs = pickle.load(open("tasks.dat", "rb"))

    response["jobs"] = jobs

    return render(request, "Analyzer/Jobs.html", response)


def loadtest(request):
    return loadtest_jmeter(request)


def loadtest_jmeter(request):
    user = User(get_client_ip(request))
    task = Task(0)

    jm = JMeter({
        "-n": "",
        "-t": ANALYSIS_PATH + "JMeter.jmx",
        "-l": user.hash + "/JM_" + task.hash + ".csv",
        "-L": "jmeter.util=WARN"
    })
    jm.arg_separator = " "

    task.set(jm.execute, {"path": "/home/chris/Programme/apache-jmeter-4.0/bin/"})
    scheduler.add(task)

    conf = dict(jm.config)
    del conf["-t"]
    del conf["-l"]

    response = RESPONSE
    response["mail"] = user.mail
    response["tool"] = jm.name
    response["config"] = json.dumps(conf, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def loadtest_locust(request):
    user = User(get_client_ip(request))
    task = Task(0)

    lc = Locust({
        "-f":             ANALYSIS_PATH + "Locust.py",
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

    task.set(lc.execute)
    scheduler.add(task)

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
