from locust import HttpLocust, TaskSet, events
from time import time


def index(l):
    l.client.get("/")


class DomainTaskSet(TaskSet):
    tasks = [index]


class LocustRun(HttpLocust):
    host = "www.example.com"
    result_file = "Vizard/resource/tests/LC_" + str(time()) + ".csv"
    min_wait = 2000
    max_wait = 5000
    task_set = DomainTaskSet
    header = ["timeStamp", "service", "type", "success", "responseTime", "bytes"]
    footer = ["www.example.com"]
    data = []
    last_entry = 0

    def __init__(self):
        super().__init__()

        events.request_success += self.save_succ
        events.request_failure += self.save_fail
        events.quitting += self.write

    def save_succ(self, request_type, name, response_time, response_length):
        self.save(request_type, name, response_time, response_length, 1)

    def save_fail(self, request_type, name, response_time):
        self.save(request_type, name, response_time, 0, 0)

    def save(self, request_type, name, response_time, response_length, success):
        timestamp = int(round(time() * 1000))
        if timestamp != self.last_entry:
            self.data.append([timestamp, name, request_type, success, response_time, response_length])
            self.last_entry = timestamp

    def write(self):
        with open(self.result_file, 'wb') as csv_file:
            csv_file.write(bytes(','.join(self.header) + "\n", "utf-8"))
            for value in self.data:
                csv_file.write(bytes(','.join(str(x) for x in value) + "\n"))
            csv_file.write(bytes(','.join(self.footer) + "\n"))
