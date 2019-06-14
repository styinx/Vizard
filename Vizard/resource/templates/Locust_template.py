import json
from locust import HttpLocust, TaskSet, events
from time import time


def index(l):
    l.client.get('/')


class DomainTaskSet(TaskSet):
    tasks = [index]


class LocustRun(HttpLocust):
    result_file = '$RESULT_FILE'
    min_wait = $MIN_WAIT
    max_wait = $MAX_WAIT
    task_set = DomainTaskSet
    header = ['timeStamp', 'service', 'type', 'success', 'responseTime', 'bytes']
    data = {}
    last_entry = 0

    def __init__(self):
        super().__init__()

        events.request_success += self.save_succ
        events.request_failure += self.save_fail
        events.quitting += self.write

    @staticmethod
    def success(result):
        if result:
            return 'true'
        return 'false'

    def save_succ(self, request_type, name, response_time, response_length):
        self.save(request_type, name, response_time, response_length, 1)

    def save_fail(self, request_type, name, response_time):
        self.save(request_type, name, response_time, 0, 0)

    def save(self, request_type, name, response_time, response_length, success):
        timestamp = int(round(time() * 1000))
        if timestamp != self.last_entry:
            success = LocustRun.success(success)
            self.data[int(timestamp)] = [name, request_type, success, response_time, response_length]
            self.last_entry = timestamp

    def write(self):
        open(self.result_file, 'w').write(json.dumps(self.data))
