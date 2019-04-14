import pickle
import os
from time import sleep, time
from threading import Lock, Thread
from shutil import rmtree

from Vizard.settings import TASK_PATH
from source.util import hash


user_save_lock = Lock()
user_task_lock = Lock()


class User:
    def __init__(self, ip):
        self.ip = ip
        self.mail = "asd"
        self.config = {"email": "", "pro": False, "tasks": {}}
        self.hash = hash(ip)

        self.load()

    def __del__(self):
        self.save()

    def setTask(self, task, status="", started=0, completed=0):
        user_task_lock.acquire()
        if task.hash not in self.config["tasks"]:
            self.config["tasks"][task.hash] = {"status": "", "started": 0, "completed": 0}

        if status != "":
            self.config["tasks"][task.hash]["status"] = status

        if started != 0:
            self.config["tasks"][task.hash]["started"] = started

        if completed != 0:
            self.config["tasks"][task.hash]["completed"] = completed

        user_task_lock.release()
        self.save()

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
        self.kwargs = kwargs

        self.path = TASK_PATH + "/" + self.hash + "/"
        if os.path.exists(self.path):
            rmtree(self.path)

        os.makedirs(self.path)

    def setExecutionCallback(self, callback, kwargs=None):
        self.execution_callback = callback
        self.hash = hash(self.time)
        self.kwargs = kwargs

    def setProcessingCallback(self, callback):
        self.processing_callback = callback

    def __call__(self):
        if self.execution_callback is not None:
            if self.kwargs is not None:
                self.execution_callback(**self.kwargs)
            else:
                self.execution_callback()

            if self.processing_callback is not None:
                self.processing_callback()


class TaskScheduler:
    def __init__(self):
        self.lock = Lock()
        self.queue = []
        self.poll_interval = 5

    def addTask(self, task, user):
        self.lock.acquire()
        self.queue.append({user: task})
        user.setTask(task, status="pending")
        self.lock.release()

    def run(self):
        while True:
            if len(self.queue) > 0:
                self.lock.acquire()
                (user, task), = self.queue.pop(0).items()
                self.lock.release()
                thread = Thread(target=task)
                thread.start()

                user.setTask(task, status="running", started=time())

                thread.join()

                user.setTask(task, status="complete", completed=time())
                user.save()

            else:
                sleep(self.poll_interval)
