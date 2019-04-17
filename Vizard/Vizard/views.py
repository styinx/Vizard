from django.shortcuts import render

from Vizard.models import User
from Vizard.settings import RESPONSE


def home(request):
    return render(request, "Home.html")


def details(request):
    return render(request, "Details.html")


def documentation(request):
    return render(request, "Documentation.html")


def my(request, what=""):
    user = User(request)
    response = RESPONSE.copy()

    if what == "tasks":
        response["tasks"] = user.getTasks()

    elif what == "reports":
        response["reports"] = "TODO, nothing to see"

    return render(request, "My.html", response)
