import json
from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User, Task, TaskScheduler
from Vizard.settings import RESOURCE_PATH, RESPONSE, TEMPLATE_PATH, JMETER_NAME
from Analyzer.models import Testplan, JMeter, Locust, Vizardplan

scheduler = TaskScheduler()
scheduler_thread = Thread(target=scheduler.run)
scheduler_thread.daemon = True
scheduler_thread.start()


def unpack_values(request, d):
    missing_values = []
    values = d.copy()
    possible_values = values.keys()

    for k, v in request.GET.items():
        if k in possible_values:
            values[k] = v

    for k, v in values.items():
        if v is None:
            missing_values.append(k)

    if missing_values:
        return missing_values

    return values


def unpack_loadtest_values(request):
    return unpack_values(request, {
        "domain": None,
        "port": "",
        "duration": "10",
        "load": "10",

        # jmeter
        "ramp_up": "1",
        "ramp_down": "1",

        # locust
        "min_wait": "1000",
        "max_wait": "2000",
        "hatch_rate": "1"
    })


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
    response = RESPONSE.copy()
    task = Task(0)
    user = User(request)
    user.setTask(task, path=task.hash)

    values = unpack_loadtest_values(request)

    if isinstance(values, list):
        response["missing"] = ', '.join(values)
        return render(request, "Analyzer/Analysis.html", response)

    result_file = task.path + "/result.csv"
    experiment_file = task.path + "/experiment.jmx"
    loadtest_arguments = {
        "$DOMAIN":      values["domain"],
        "$THREADS":     values["load"],
        "$DURATION":    values["duration"],
        "$RESULT_FILE": result_file}

    vizard_configuration = {
        "tool":       "JMeter",
        "experiment": experiment_file,
        "task":       task.hash,
        "arguments":  loadtest_arguments
    }

    Vizardplan(task.path + "/vizard.json", vizard_configuration)
    testplan = Testplan(TEMPLATE_PATH + "/JMeter_template.jmx", experiment_file, loadtest_arguments)

    jm = JMeter({
        "-n": "",
        "-t": testplan.target,
        "-L": "jmeter.util=WARN"
    })
    jm.arg_separator = " "

    task.setExecutionCallback(jm.execute, {"path": RESOURCE_PATH + "/" + JMETER_NAME + "/bin/"})
    task.setProcessingCallback(jm.process, {"path": result_file})
    scheduler.addTask(task, user)

    conf = dict(jm.config)
    del conf["-t"]

    response["mail"] = user.mail
    response["tool"] = jm.name
    response["config"] = json.dumps(conf, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def loadtest_locust(request):
    response = RESPONSE.copy()
    task = Task(0)
    user = User(request)
    user.setTask(task, path=task.hash)

    values = unpack_loadtest_values(request)

    if isinstance(values, list):
        response["missing"] = ', '.join(values)
        return render(request, "Analyzer/Analysis.html", response)

    experiment_file = task.path + "/experiment.py"
    loadtest_arguments = {
        "$MIN_WAIT":    values["min_wait"],
        "$MAX_WAIT":    values["max_wait"],
        "$RESULT_FILE": task.path + "/result_processed.json"}

    vizard_configuration = {
        "tool":       "Locust",
        "experiment": experiment_file,
        "task":       task.hash,
        "arguments":  loadtest_arguments
    }

    Vizardplan(task.path + "/vizard.json", vizard_configuration)
    testplan = Testplan(TEMPLATE_PATH + "/Locust_template.py", experiment_file, loadtest_arguments)

    lc = Locust({
        "-f":             testplan.target,
        "--csv":          task.path + "/",
        "--no-web":       "",
        "--only-summary": "",
        "-H":             values["domain"],
        # "-P":             values["port"],
        "-L":             "CRITICAL",
        "-c":             values["load"],
        "-t":             values["duration"] + 's',
        "-r":             values["hatch_rate"]
    })
    lc.arg_separator = " "

    task.setExecutionCallback(lc.execute)
    scheduler.addTask(task, user)

    conf = dict(lc.config)
    del conf["--csv"]
    del conf["-f"]

    response["mail"] = user.mail
    response["tool"] = lc.name
    response["config"] = json.dumps(conf, indent=2)
    response["hash"] = task.hash

    return render(request, "Analyzer/Analysis.html", response)


def stresstest(request):
    return HttpResponse("")
