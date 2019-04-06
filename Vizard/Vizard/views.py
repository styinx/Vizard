import json
from hashlib import sha1

from django.shortcuts import render

from Vizard.models import User
from source.util import get_client_ip


def index(request):
    return render(request, "Index.html")


def details(request):
    return render(request, "Details.html")


def documentation(request):
    return render(request, "Documentation.html")


def user(request, _user):
    ip = get_client_ip(request)
    if sha1(ip.encode()).hexdigest()[:8] != _user:
        return render(request, "Index.html")

    else:
        user_obj = User(ip)

        for key in request.GET:
            if key in user_obj.config:
                user_obj.config[key] = request.GET[key]

        user_obj.save()

        return render(request, "User.html", {"user": json.dumps(user_obj.config, indent=2)})
