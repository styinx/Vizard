from django.http import HttpResponse
from django.shortcuts import render

from Vizard.settings import RESPONSE
from Presenter.report import collect_data, collect_report


def index(request):
    return render(request, "Presenter/Index.html")


def data(request, api="", _id=""):
    response = collect_data(request, RESPONSE.copy(), api, _id)

    if api:
        return HttpResponse(response)

    return render(request, "Presenter/Data.html", response)


def report_id(request, _id, export=None):
    response = collect_report(request, RESPONSE.copy(), _id, export)

    return render(request, "Presenter/Report.html", response)
