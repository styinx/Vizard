import os
import json
from hashlib import sha1


class User:
    def __init__(self, ip):
        self.ip = ip
        self.mail = "asd"
        self.config = {"email": "", "pro": False, "tasks": [{"id": 0, "started": 0, "completed": 0}]}
        self.hash = self.hash()

        self.load()

    def hash(self):
        return sha1(self.ip.encode()).hexdigest()[:8]

    def create(self):
        if not os.path.exists(self.hash):
            os.mkdir(self.hash)

        open(self.hash + "/config.json", "w+").close()

    def save(self):
        self.create()

        f = open(self.hash + "/config.json", "w")
        f.write(json.dumps(self.config))

    def load(self):
        self.create()

        buffer = open(self.hash + "/config.json", "r").read()
        if buffer:
            self.config = json.loads(buffer)
