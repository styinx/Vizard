import pickle
import os
from time import sleep, time
from threading import Lock, Thread

from source.util import hash


task_lock = Lock()


class Task:
    def __init__(self, delay=0, callback=None, kwargs=None):
        self.callback = callback
        self.time = time() + delay
        self.hash = hash(self.time)
        self.kwargs = kwargs

    def setCallback(self, callback, kwargs=None):
        self.callback = callback
        self.hash = hash(self.time)
        self.kwargs = kwargs

    def __call__(self):
        if self.callback is not None:
            if self.kwargs is not None:
                self.callback(**self.kwargs)
            else:
                self.callback()


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
