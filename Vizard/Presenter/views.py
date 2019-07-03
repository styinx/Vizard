from django.http import HttpResponse
from django.shortcuts import render

from Vizard.settings import RESPONSE
from Presenter.report import collect_data, collect_report, collect_report_result


def index(request):
    return render(request, 'Presenter/Index.html')


def data(request, api='', _id=''):
    response = collect_data(request, RESPONSE.copy(), api, _id)

    if api:
        return HttpResponse(response)

    return render(request, 'Presenter/Data.html', response)


def report_id(request, api='', _id='', export=None):
    response, zipped = collect_report(request, RESPONSE.copy(), _id, export)

    if api:
        return HttpResponse(collect_report_result(request, response, _id))

    if export == "export":
        response = HttpResponse(zipped[1], content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + zipped[0]
        return response

    return render(request, 'Presenter/Report.html', response)


def report_compare(request, api='', compare='', export=None):
    id1, id2 = compare.split('-')


    return HttpResponse('todo')
    #return render(request, 'Presenter/Compare.html', response)
