import os
import pickle
from source.util import hash


class User:
    def __init__(self, ip):
        self.ip = ip
        self.mail = "asd"
        self.config = {"email": "", "pro": False, "tasks": [{"id": 0, "started": 0, "completed": 0}]}
        self.hash = hash(ip)

        self.load()

    def __del__(self):
        self.save()

    def create(self):
        if not os.path.exists(self.hash):
            os.mkdir(self.hash)

        if not os.path.exists(self.hash + "/config.dat"):
            pickle.dump(self.config, open(self.hash + "/config.dat", "wb"))

    def save(self):
        self.create()

        pickle.dump(self.config, open(self.hash + "/config.dat", "wb"))

    def load(self):
        self.create()

        self.config = pickle.load(open(self.hash + "/config.dat", "rb"))
