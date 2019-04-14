from django.shortcuts import render

from Vizard.settings import RESPONSE


def home(request):
    return render(request, "Home.html")


def details(request):
    return render(request, "Details.html")


def documentation(request):
    return render(request, "Documentation.html")


def my(request, what=""):
    response = RESPONSE

    if what == "tasks":
        response["tasks"] = "blabla tasks"

    elif what == "reports":
        response["reports"] = "bla bla reports"

    return render(request, "My.html", response)
