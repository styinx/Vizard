import os
from requests import post
from time import sleep, time
from threading import Lock, Thread
from shutil import rmtree

from source.util import hash_id, get_client_ip, serialize, unserialize

from Vizard.settings import TASK_PATH, MAX_THREADS, USER_PATH

user_save_lock = Lock()
user_task_lock = Lock()


class User:
    def __init__(self, request):
        self.ip = get_client_ip(request)
        self.config = {'email': '', 'pro': False, 'tasks': {}}
        self.hash = hash_id(self.ip)
        self.registered = False

        if not self.registered:
            self.hash = '0xffffffff'

        self.load()

    def __del__(self):
        self.save()

    def set_task(self, task, status='', started=0, completed=0, path=''):
        user_task_lock.acquire()

        if task.hash not in self.config['tasks']:
            self.config['tasks'][task.hash] = {'status': '', 'started': 0, 'completed': 0, 'path': ''}

        if status != '':
            self.config['tasks'][task.hash]['status'] = status

        if started != 0:
            self.config['tasks'][task.hash]['started'] = started

        if completed != 0:
            self.config['tasks'][task.hash]['completed'] = completed

        if path != '':
            self.config['tasks'][task.hash]['path'] = path

        user_task_lock.release()
        self.save()

    def get_tasks(self):
        return self.config['tasks']

    def create(self):
        path = USER_PATH + '/' + self.hash
        file = path + '/config.dat'

        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(file):
            serialize(self.config, file)

    def save(self):
        self.create()

        user_save_lock.acquire()
        serialize(self.config, USER_PATH + '/' + self.hash + '/config.dat')
        user_save_lock.release()

    def load(self):
        self.create()

        self.config = unserialize(USER_PATH + '/' + self.hash + '/config.dat')

    def valid(self, task):
        if task in self.config['tasks']:
            return True
        return False


class Task:
    def __init__(self, delay=0, callback=None, kwargs=None):
        self.execution_callback = callback
        self.processing_callback = None
        self.analyzer = None
        self.time = time() + delay
        self.hash = hash_id(self.time)
        self.e_kwargs = kwargs
        self.p_kwargs = kwargs

        self.path = TASK_PATH + '/' + self.hash

    def create_path(self):
        if os.path.exists(self.path):
            rmtree(self.path)

        os.makedirs(self.path)

    def set_execution_callback(self, callback, kwargs=None):
        self.execution_callback = callback
        self.e_kwargs = kwargs

    def set_processing_callback(self, callback, kwargs=None):
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
        self.api_callback = {}
        self.active_tasks = 0
        self.poll_interval = 3

    def add_task(self, task, user):
        self.lock.acquire()
        self.queue.append({user: task})
        user.set_task(task, status='pending')
        self.lock.release()

    def add_task_callback(self, _hash, url):
        self.api_callback[_hash] = url

    def run(self):
        while True:
            if len(self.queue) > 0 and self.active_tasks < MAX_THREADS:
                self.lock.acquire()
                (user, task), = self.queue.pop(0).items()
                self.active_tasks += 1
                self.lock.release()

                thread = Thread(target=task)
                thread.start()

                user.set_task(task, status='running', started=time())

                thread.join()

                if task.hash in self.api_callback:
                    post(self.api_callback[task.hash])

                user.set_task(task, status='complete', completed=time())
                user.save()

                self.lock.acquire()
                self.active_tasks -= 1
                self.lock.release()

            else:
                sleep(self.poll_interval)
