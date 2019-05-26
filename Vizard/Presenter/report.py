import os
import json
import shutil
from time import strftime, gmtime

from django.template.loader import render_to_string

from source.util import dump, pack_zip, write

from Vizard.settings import RESPONSE, TASK_PATH, STATIC_URL, BASE_DIR, DATE_FORMAT
from Vizard.models import User


def collect_data(request, response, api, _id):
    user = User(request)

    if _id:
        if user.valid(_id):
            data = json.loads(open(TASK_PATH + "/" + _id + "/result_processed.json").read())

            response["task"] = _id
            response["data"] = dump(data)
            return response

        response["status"] = "404"
        response["message"] = "Sorry, the requested job id (" + str(_id) + ") seems not to exists."

        return response

    if api:
        response["experiments"] = {}
        tasks_info = user.getTasks()
        for experiment in tasks_info:
            response["experiments"][experiment] = open(TASK_PATH + "/" + experiment + "/re", )

        if _id:
            return dump(response["experiments"][_id])

        return dump(response["experiments"])

    response["experiments"] = {}

    tasks_info = user.getTasks()
    for experiment in tasks_info:
        started = strftime(DATE_FORMAT, gmtime(tasks_info[experiment]["started"]))
        completed = strftime(DATE_FORMAT, gmtime(tasks_info[experiment]["completed"]))
        response["experiments"][experiment] = {"started": started, "completed": completed}

    return response


def collect_report(request, response, _id, export):
    user = User(request)

    response["hash"] = _id
    response["metrics"] = {}

    if _id in user.getTasks():
        task = user.getTasks()[_id]
        path = TASK_PATH + "/" + task["path"]
        config = open(path + "/vizard.json", "r")
        data_blob = json.loads(open(path + "/result_processed.json", "r").read())

        values = [[int(ts), round(float(data_blob[ts][3]), 2)] for ts in data_blob]

        response["metrics"]["asdasdasd"] = {
            "data": values,
            "text": "blasdasd as as"
        }

        if export is None:
            return response

        else:
            export_report(response, path, _id)
            return response

    else:
        response["status"] = "404"
        response["message"] = "Sorry, the requested id (" + str(_id) + ") seems not to exists."
        return response


def export_report(response, path, _id):
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
    shutil.copy(static_url + "js/util.js", static_path + "/js/util.js")

    html_content = render_to_string("Presenter/Report.html", response).replace("/static/", "./static/")

    write(export_path + "/Report.html", html_content)
    pack_zip(path + "/" + _id + ".zip", export_base)
