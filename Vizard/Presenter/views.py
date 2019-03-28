from django.shortcuts import render

from Vizard.models import User
from source.util import get_client_ip


def index(request):
    return render(request, "Presenter/Index.html")


def data(request):
    response = {
        "status":  "",
        "message": "",
        "data_entries": ["056", "5613"]
    }

    user = User(get_client_ip())

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
    response = {
        "status":  "",
        "message": "",
        "id":      _id
    }

    if 1:
        response["status"] = "404"

    return render(request, "Presenter/Report.html", response)
