import json
import os
import shutil
from time import strftime, gmtime

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from Vizard.settings import RESPONSE, TASK_PATH, STATIC_URL, BASE_DIR
from Vizard.models import User


def index(request):
    return render(request, "Presenter/Index.html")


def data(request, api="", _id=""):
    response = RESPONSE.copy()
    user = User(request)

    if api:
        if _id:
            return HttpResponse("<body>{" + api + ": \"here will be some data from id\"}</body>")

        return HttpResponse("<body>{" + api + ": \"here will be some data from all jobs\"}</body>")

    if _id:
        if user.valid(_id):
            data = json.loads(open(TASK_PATH + "/" + _id + "/result_processed.json").read())

            response["task"] = _id
            response["data"] = json.dumps(data, indent=2)
            return render(request, "Presenter/Data.html", response)

        response["status"] = "404"
        response["message"] = "Sorry, the requested job id (" + str(_id) + ") seems not to exists."

        return render(request, "util/error.html", response)

    response["experiments"] = {}

    tasks = user.getTasks()
    for experiment in tasks:
        started = strftime("%H:%M:%S %d/%m/%Y", gmtime(tasks[experiment]["started"]))
        completed = strftime("%H:%M:%S %d/%m/%Y", gmtime(tasks[experiment]["completed"]))
        response["experiments"][experiment] = {"started": started, "completed": completed}

    return render(request, "Presenter/Data.html", response)


def report_id(request, _id, export=None):
    user = User(request)
    response = RESPONSE.copy()

    response["hash"] = _id
    response["metrics"] = {}

    if _id in user.getTasks():
        task = user.getTasks()[_id]
        path = TASK_PATH + "/" + task["path"]
        config = open(path + "/vizard.json", "r")
        data_blob = json.loads(open(path + "/result_processed.json", "r").read())

        values = [[int(ts), round(data_blob[ts][3], 2)] for ts in data_blob]

        response["metrics"]["asdasdasd"] = {
            "data": values,
            "text": "blasdasd as as"
        }

        if export is None:
            return render(request, "Presenter/Report.html", response)

        else:
            export_base = path + "/export"
            export_path = export_base + "/" + _id
            static_path = export_path + "/static"
            static_url = BASE_DIR + "/" + STATIC_URL

            if os.path.exists(export_base):
                shutil.rmtree(export_base)
            os.makedirs(static_path)
            os.mkdir(static_path + "/css")
            os.mkdir(static_path + "/js")

            shutil.copy(static_url + "css/bootstrap.min.css", static_path + "/css/bootstrap.min.css")
            shutil.copy(static_url + "js/jquery.min.js", static_path + "/js/jquery.min.js")
            shutil.copy(static_url + "js/highstock.js", static_path + "/js/highstock.js")
            shutil.copy(static_url + "js/charts.js", static_path + "/js/charts.js")

            html_content = render_to_string("Presenter/Report.html", response).replace("/static/", "./static/")

            open(export_path + "/Report.html", "w").write(html_content)

            if os.path.exists(path + "/" + _id + ".zip"):
                os.remove(path + "/" + _id + ".zip")

            shutil.make_archive(path + "/" + _id, "zip", export_base)

            return render(request, "util/error.html", {"status": 200, "message": "All good, archive created; download not yet supported"})

    else:
        response["status"] = "404"
        response["message"] = "Sorry, the requested id (" + str(_id) + ") seems not to exists."

        return render(request, "util/error.html", response)
