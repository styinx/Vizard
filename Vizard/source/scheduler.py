from time import sleep, time
from threading import Lock, Thread
import pickle
import os

from source.util import hash


class Task:
    def __init__(self, delay=0, callback=None, kwargs=None):
        self.callback = callback
        self.time = time() + delay
        self.hash = hash(self.time)
        self.kwargs = kwargs

        self.log("pending")

    def log(self, status):
        tasks = {}
        if not os.path.exists("tasks.dat"):
            pickle.dump({}, open("tasks.dat", "wb"))

        else:
            tasks = pickle.load(open("tasks.dat", "rb"))

        tasks[self.hash] = status

        pickle.dump(tasks, open("tasks.dat", "wb"))

    def set(self, callback, kwargs=None):
        self.callback = callback
        self.hash = hash(self.time)
        self.kwargs = kwargs

        self.log("pending")

    def __call__(self):
        if self.callback is not None:
            self.log("running")
            if self.kwargs is not None:
                self.callback(**self.kwargs)
            else:
                self.callback()


class TaskScheduler:
    def __init__(self):
        self.lock = Lock()
        self.queue = []
        self.poll_interval = 5

    def add(self, task):
        self.lock.acquire()
        self.queue.append(task)
        self.lock.release()

    def run(self):
        while True:
            if len(self.queue) > 0:
                self.lock.acquire()
                task = self.queue.pop(0)
                self.lock.release()
                thread = Thread(target=task)
                thread.start()
                thread.join()

                task.log("done")

            else:
                sleep(self.poll_interval)
