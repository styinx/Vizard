import re


class Series:
    def __init__(self, values=None):
        self.index = 0
        self.key = 0
        self.values = {}

        self.__iadd__(values)

    def __iadd__(self, other):
        self.add(other)
        return self

    def __str__(self):
        return str(self.values)

    def clear(self):
        self.index = 0
        self.key = 0
        self.values = {}
        return self

    def add(self, args):
        if isinstance(args, int):
            self.addValue(args)
        elif isinstance(args, tuple):
            self.addTuple(args)
        elif isinstance(args, list):
            self.addList(args)
        elif isinstance(args, dict):
            self.addDict(args)
        elif isinstance(args, str):
            self.addStr(args)
        return self

    def addValue(self, *args):
        index, value, key = self.index, None, ""

        if len(args) > 0:

            if len(args) == 1:
                if isinstance(args[0], int) or isinstance(args[1], float):
                    value = args[0]
            if len(args) >= 2:
                if isinstance(args[0], int):
                    index = args[0]
                if isinstance(args[1], float) or isinstance(args[1], int) or isinstance(args[1], list) or isinstance(args[1], dict):
                    value = args[1]
                elif isinstance(args[1], str):
                    key = args[1]
            if len(args) == 3:
                if isinstance(args[2], float) or isinstance(args[2], int) or isinstance(args[1], list) or isinstance(args[1], dict):
                    value = args[2]
                elif isinstance(args[2], str):
                    key = args[2]

            if key != "":
                self.values[index] = {key: value}
            else:
                self.values[index] = value

            self.index = index + 1

        return self

    def addTuple(self, args):
        if isinstance(args, tuple):
            self.addValue(*args)

        return self

    def addList(self, args):
        if isinstance(args, list):
            for entry in args:
                self.add(entry)

        return self

    def addDict(self, args):
        if isinstance(args, dict):
            for key in args:
                if isinstance(key, int):
                    if isinstance(args[key], int):
                        self.addValue(key, args[key])
                    elif isinstance(args[key], dict):
                        self.addValue(key, args[key])

        return self

    def addStr(self, args):
        if isinstance(args, str):
            _range = re.match(r"(\d+):(\d+)(:(\d+))", args)
            while _range:
                groups = _range.groups()
                start, stop, step = int(groups[0]), int(groups[1]), 1
                if len(groups) == 4:
                    step = int(groups[3])
                self.addList(list(range(start, stop, step)))
                args = re.sub(r"(\d+):(\d+)(:(\d+))", "", args)
                _range = re.match(r"(\d+):(\d+)(:(\d+))", args)
                print(list(range(start, stop, step)))
        return self
