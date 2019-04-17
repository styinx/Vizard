from random import randint
from time import strftime, gmtime

from django.http import HttpResponse
from django.shortcuts import render

from Vizard.settings import RESPONSE
from Vizard.models import User


def index(request):
    return render(request, "Presenter/Index.html")


def data(request, api="", _id=""):
    response = RESPONSE.copy()
    user = User(request)

    if api:
        if _id:
            return HttpResponse("<body>{" + api + ": \"here will be some data from id\"}</body>")

        return HttpResponse("<body>{" + api + ": \"here will be some data from all jobs\"}</body>")

    if _id:
        if user.valid(_id):
            response["task"] = _id
            return render(request, "Presenter/Data.html", response)

        response["status"] = "404"
        response["message"] = "Sorry, the requested job id (" + str(_id) + ") seems not to exists."

        return render(request, "error.html", response)

    response["experiments"] = {}

    tasks = user.config["tasks"]
    for experiment in tasks:
        started = strftime("%H:%M:%S %d/%m/%Y", gmtime(tasks[experiment]["started"]))
        completed = strftime("%H:%M:%S %d/%m/%Y", gmtime(tasks[experiment]["completed"]))
        response["experiments"][experiment] = {"started": started, "completed": completed}

    return render(request, "Presenter/Data.html", response)


def report_id(request, _id):
    response = RESPONSE.copy()

    response["hash"] = _id
    response["metrics"] = {
        "resp": {
            "data": list(range(100000)),
            "text": "some metric text"
        },
        "asd": {
            "data": [[x, randint(50, 120)] for x in range(1533861124, 1533881124, 1000)],
            "text": "some metric text number 2 enhanced"
        }}

    return render(request, "Presenter/Report.html", response)
