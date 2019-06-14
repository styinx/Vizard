from django.shortcuts import render

from Vizard.models import User
from Vizard.settings import RESPONSE


def home(request):
    return render(request, 'Home.html')


def details(request):
    return render(request, 'Details.html')


def documentation(request):
    return render(request, 'Documentation.html')


def bot(request):
    return render(request, 'Bot.html')


def demo(request):
    return render(request, 'Demo.html')


def my(request, what=''):
    user = User(request)
    response = RESPONSE.copy()

    if what == 'tasks':
        response['tasks'] = user.get_tasks()

    elif what == 'reports':
        response['reports'] = 'TODO, nothing to see'

    response['hash'] = user.hash

    return render(request, 'My.html', response)
