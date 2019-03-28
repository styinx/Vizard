from time import sleep, time
from threading import Lock, Thread
from hashlib import sha1


class Task:
    def __init__(self, callback, delay, *args, **kwargs):
        self.callback = callback
        self.time = time() + delay
        self.hash = self.hash()
        self.args = args
        self.kwargs = kwargs

    def hash(self):
        return sha1(str(self.time).encode()).hexdigest()[:8]

    def __call__(self):
        self.callback(*self.args, **self.kwargs)


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
                thread.daemon = True
                thread.start()

            else:
                sleep(self.poll_interval)
