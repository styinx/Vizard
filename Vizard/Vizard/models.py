import os
import pickle
from threading import Lock

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
