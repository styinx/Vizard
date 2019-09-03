from django.http import HttpResponse
from django.shortcuts import render

from Vizard.models import User
from Vizard.settings import RESPONSE
from source.util import dump


def home(request):
    return render(request, 'Home.html')


def details(request):
    return render(request, 'Details.html')


def documentation(request):
    return render(request, 'Documentation.html')


def bot(request):
    return render(request, 'Bot.html')


def performance_report(request):
    return render(request, '48b49d70/Report.html')


def demo_report_loadtest(request):
    return render(request, 'DemoLoadtest.html')


def demo_report_regressiontest(request):
    return render(request, 'DemoRegressiontest.html')


def webhook(request):
    print(dump(request.POST))
    return HttpResponse(dump(request.POST))


def my(request, what=''):
    user = User(request)
    response = RESPONSE.copy()

    if what == 'tasks':
        response['tasks'] = user.get_tasks()

    elif what == 'reports':
        response['reports'] = 'TODO, nothing to see'

    response['hash'] = user.hash

    return render(request, 'My.html', response)
