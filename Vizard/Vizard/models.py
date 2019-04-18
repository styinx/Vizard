import pickle
import os
from time import sleep, time
from threading import Lock, Thread
from shutil import rmtree

from Vizard.settings import TASK_PATH, MAX_THREADS
from source.util import hash, get_client_ip

user_save_lock = Lock()
user_task_lock = Lock()


class User:
    def __init__(self, request):
        self.ip = get_client_ip(request)
        self.mail = "asd"
        self.config = {"email": "", "pro": False, "tasks": {}}
        self.hash = hash(self.ip)

        self.load()

    def __del__(self):
        self.save()

    def setTask(self, task, status="", started=0, completed=0, path=""):
        user_task_lock.acquire()

        if task.hash not in self.config["tasks"]:
            self.config["tasks"][task.hash] = {"status": "", "started": 0, "completed": 0, "path": ""}

        if status != "":
            self.config["tasks"][task.hash]["status"] = status

        if started != 0:
            self.config["tasks"][task.hash]["started"] = started

        if completed != 0:
            self.config["tasks"][task.hash]["completed"] = completed

        if path != "":
            self.config["tasks"][task.hash]["path"] = path

        user_task_lock.release()
        self.save()

    def getTasks(self):
        return self.config["tasks"]

    def create(self):
        if not os.path.exists(self.hash):
            os.mkdir(self.hash)

        if not os.path.exists(self.hash + "/config.dat"):
            pickle.dump(self.config, open(self.hash + "/config.dat", "wb"))

    def save(self):
        self.create()

        user_save_lock.acquire()
        pickle.dump(self.config, open(self.hash + "/config.dat", "wb"))
        user_save_lock.release()

    def load(self):
        self.create()

        self.config = pickle.load(open(self.hash + "/config.dat", "rb"))

    def valid(self, task):
        if task in self.config["tasks"]:
            return True
        return False


class Task:
    def __init__(self, delay=0, callback=None, kwargs=None):
        self.execution_callback = callback
        self.processing_callback = None
        self.analyzer = None
        self.time = time() + delay
        self.hash = hash(self.time)
        self.e_kwargs = kwargs
        self.p_kwargs = kwargs

        self.path = TASK_PATH + "/" + self.hash
        if os.path.exists(self.path):
            rmtree(self.path)

        os.makedirs(self.path)

    def setExecutionCallback(self, callback, kwargs=None):
        self.execution_callback = callback
        self.e_kwargs = kwargs

    def setProcessingCallback(self, callback, kwargs=None):
        self.processing_callback = callback
        self.p_kwargs = kwargs

    def __call__(self):
        if self.execution_callback is not None:
            if self.e_kwargs is not None:
                self.execution_callback(**self.e_kwargs)
            else:
                self.execution_callback()

            if self.processing_callback is not None:
                if self.p_kwargs is not None:
                    self.processing_callback(**self.p_kwargs)
                else:
                    self.processing_callback()


class TaskScheduler:
    def __init__(self):
        self.lock = Lock()
        self.queue = []
        self.active_tasks = 0
        self.poll_interval = 3

    def addTask(self, task, user):
        self.lock.acquire()
        self.queue.append({user: task})
        user.setTask(task, status="pending")
        self.lock.release()

    def run(self):
        while True:
            if len(self.queue) > 0 and self.active_tasks < MAX_THREADS:
                self.lock.acquire()
                (user, task), = self.queue.pop(0).items()
                self.active_tasks += 1
                self.lock.release()

                thread = Thread(target=task)
                thread.start()

                user.setTask(task, status="running", started=time())

                thread.join()

                user.setTask(task, status="complete", completed=time())
                user.save()

                self.lock.acquire()
                self.active_tasks -= 1
                self.lock.release()

            else:
                sleep(self.poll_interval)
