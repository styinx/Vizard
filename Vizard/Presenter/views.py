from os import listdir
from random import random, randint

from django.shortcuts import render

from Vizard.models import User
from source.util import get_client_ip

from Vizard.settings import BASE_DIR, RESPONSE


def index(request):
    return render(request, "Presenter/Index.html")


def data(request):
    response = RESPONSE

    user = User(get_client_ip(request))

    response["user"] = user.hash
    response["experiments"] = []

    for analysis in listdir(BASE_DIR + "/" + user.hash):
        response["experiments"].append(analysis)

    return render(request, "Presenter/Report_List.html", response)


def data_id(request, _id):
    response = {
        "status":  "",
        "message": "",
        "id":      _id
    }

    if 1:
        response["status"] = "404"
        response["message"] = "Sorry, the requested job id (" + str(_id) + ") seems not to exists."

    return render(request, "error.html", response)


def report(request):
    response = {
        "status":  "",
        "message": ""
    }

    if 1:
        response["status"] = "404"

    return render(request, "Presenter/Report.html", response)


def report_id(request, _id):
    response = RESPONSE

    response["hash"] = _id
    response["metrics"] = {
        "resp": {
            "data" : list(range(100000)),
            "text": "some metric text"
        },
        "asd": {
            "data": [[x, randint(50, 120)] for x in range(1533861124, 1533881124, 1000)],
            "text": "some metric text number 2 enhanced"
        }}

    return render(request, "Presenter/Report.html", response)
