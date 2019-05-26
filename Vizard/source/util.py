import os
import re
import io
import sys
import json
import pickle
import shutil
import zipfile
import tarfile
import hashlib
import importlib
import urllib.request


# General methods

def hash_id(what, severity=8):
    return hashlib.sha1(str(what).encode()).hexdigest()[:severity]


def dump(json_object):
    return json.dumps(json_object, indent=2)


def path(*args):
    return '/'.join(args)


def copy_tree(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)


def pack_zip(source, filename):
    if os.path.exists(filename):
        os.remove(filename)

    shutil.make_archive(filename, source)


def unpack_zip(buffer, destination):
    zip_ref = zipfile.ZipFile(buffer)
    zip_ref.extractall(destination)
    zip_ref.close()


def unpack_url_zip(url, destination):
    unpack_url_zip(io.BytesIO(urllib.request.urlopen(url).read()), destination)


def unpack_tar(buffer, destination):
    archive = tarfile.open(fileobj=buffer)
    archive.extractall(destination)
    archive.close()


def unpack_url_tar(url, destination):
    unpack_tar(io.BytesIO(urllib.request.urlopen(url).read()), destination)


def write(obj, filename):
    open(filename, "w").write(obj)


def read(filename):
    return open(filename, "r").read()


def serialize(obj, filename):
    pickle.dump(obj, open(filename, "wb"))


def unserialize(filename):
    return pickle.load(open(filename, "rb"))


# Django methods

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def unpack_request_values(request, d):
    missing_values = []
    values = d.copy()
    possible_values = values.keys()

    for k, v in request.GET.items():
        if k in possible_values:
            values[k] = v

    for k, v in values.items():
        if v is None:
            missing_values.append(k)

    if missing_values:
        return missing_values

    return values


#
# Enables a class to be configured via bracket notation.
#
class Configurable:
    def __init__(self, member=None):
        self.subject = self

        if member is not None and isinstance(member, dict):
            self.subject = member

    def __setitem__(self, key, value):
        if self.subject == self:
            setattr(self.subject, key, value)
        else:
            self.subject[key] = value
        return self

    def __getitem__(self, key):
        if self.subject == self:
            return getattr(self.subject, key)
        else:
            return self.subject[key]

    def __iter__(self):
        if self.subject == self:
            return iter(self.__dict__)
        else:
            return iter(self.subject)


class Executable(Configurable):
    def __init__(self, executable, configurable=None):
        self.config = configurable if configurable is not None else {}
        super().__init__(self.config)

        self.executable = executable
        self.executable_path = ""
        self.arg_separator = "="

    def execute(self, path=None):
        args = ""

        if path is not None:
            self.executable_path = path

        for arg in self.__iter__():
            args += arg
            if self.__getitem__(arg) != "":
                args += self.arg_separator + str(self.__getitem__(arg))
            args += " "

        os.system(self.executable_path + self.executable + " " + args)


class ConfigFile:
    def __init__(self, target):
        self.path = ""
        self.section = "DEFAULT"
        self.dictionary = {"DEFAULT": {}}
        self.separator = '='
        self.comments = [';', '#', "//"]
        self.bool_true = ['t', "true", 'y', "yes"]
        self.bool_false = ['f', "false", 'n', "no"]

        if os.path.exists(target):
            self.path = target
            f = open(target, mode='r', encoding="utf-8")
            self.read(f.readlines())
        else:
            self.read(target.split('\n'))

    def __iter__(self):
        return self.dictionary

    def __getitem__(self, item):
        for sec in self.dictionary:
            if item == sec:
                return self.dictionary[sec]
            for key in self.dictionary[sec]:
                if item == key:
                    return self.dictionary[sec][key]
        return -1

    def read(self, lines):
        for line in lines:
            if re.match(r"\s[" + ''.join(self.comments) + "].*", line) or re.match(r"^\s+", line):
                continue
            elif re.match(r"\[.*\]", line):
                self.section = line.replace('[', '').replace(']', '').strip()
                self.dictionary[self.section] = {}
            else:
                pair = line.split(self.separator)
                if len(pair) == 2:
                    self.dictionary[self.section][pair[0].strip()] = self.readEntry(pair[1].strip())
                elif len(pair) == 1:
                    self.dictionary[self.section][pair[0].strip()] = -1

    def readEntry(self, value):
        value = value.strip()
        if re.match(r"\d*\.\d+", value):
            return float(value)
        elif re.match(r"\d+", value):
            return int(value)
        elif re.match(r"\".*\"", value):
            return value.split('"')[1]
        elif value.lower() in self.bool_true:
            return True
        elif value.lower() in self.bool_false:
            return False
        else:
            class_path = value[0:value.find('(')].split('.')
            class_name = class_path[-1]

            value = value[value.find('(') + 1:value.rfind(')')]

            # compute nested functions recursively
            res = re.search(r"(\w+\.)*\w+\(\w+[^\(\)]*\)", value)
            if res:
                while res:
                    res_val = self.readEntry(res[0])
                    value = re.sub(r"(\w+\.)*\w+\(\w+[^\(\)]*\)", str(res_val), value)
                    res = re.search(r"(\w+\.)*\w+\(\w+[^\(\)]*\)", value)

            arguments = [str(eval(x)) for x in value.split(",")]

            # import module from string if not yet imported
            if class_name != '':
                module_name = __name__
                if len(class_path) > 1:
                    module_name = '.'.join(class_path[:-1])
                if module_name not in sys.modules.keys():
                    importlib.import_module(module_name)

                # compute complex class types and functions
                class_init = getattr(sys.modules[module_name], class_name)
                return class_init(*map(self.readEntry, arguments))
            return value
