from django.http import HttpResponse
from django.shortcuts import render

from Vizard.settings import RESPONSE
from Presenter.report import LoadtestReport, CompareReport


def index(request):
    return render(request, 'Presenter/Index.html')


def data(request, api='', _id=''):
    report = LoadtestReport(request, RESPONSE.copy(), api, _id, None)
    response = report.collect_data()

    if api:
        return HttpResponse(response)

    return render(request, 'Presenter/' + report.data_template, response)


def data_compare(request, api='', _id=''):
    id1, id2 = _id.split('-')

    report = CompareReport(request, RESPONSE.copy(), api, id1, id2, None)
    response = report.collect_data()

    if api:
        return HttpResponse(response)

    return render(request, 'Presenter/' + report.data_template, response)


def report_id(request, api='', _id='', export=None):
    report = LoadtestReport(request, RESPONSE.copy(), api, _id, export)

    response, zipped = report.collect_report()

    if api:
        return HttpResponse(report.collect_report_result())

    if export == "export":
        response = HttpResponse(zipped[1], content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + zipped[0]
        return response

    return render(request, 'Presenter/' + report.report_template, response)


def report_compare(request, api='', _id='', export=None):
    id1, id2 = _id.split('-')

    report = CompareReport(request, RESPONSE.copy(), api, id1, id2, export)

    response, zipped = report.collect_report()

    if api:
        return HttpResponse(report.collect_report_result())

    if export == "export":
        response = HttpResponse(zipped[1], content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + zipped[0]
        return response

    return render(request, 'Presenter/' + report.report_template, response)
