from source.util import Executable


class Testplan:
    def __init__(self, template, target, arguments):
        self.target = target
        self.content = open(template, "r").read()
        self.configuration = self.content

        for key, value in arguments.items():
            self.configuration = self.configuration.replace(key, value)

        open(target, "w").write(self.configuration)


class AnalyzeTool(Executable):
    def __init__(self, name, executable, arguments=None):
        super().__init__(executable, arguments)

        self.name = name

    def run(self, arguments=None):
        if arguments is not None:
            for arg in arguments:
                self.__setitem__(arg, arguments[arg])

        self.execute()

    def process(self):
        pass


class JMeter(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("JMeter", "jmeter", arguments)

    def process(self):
        result = {}
        if "-l" in self.config:
            f = open(self.config["-l"], "r")

            headers = {x: i for i, x in enumerate(f.readline()[:-1].split(","))}

            ts = -1
            if "timeStamp" in headers:
                ts = headers["timeStamp"]

            key = 0
            for line in f.readlines():
                values = list(line[:-1].split(","))

                if ts >= 0:
                    ts_val = values[ts]
                    del values[ts]
                    result[ts_val] = values
                else:
                    result[key] = values
                    key += 1
        return result


class Locust(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("Locust", "locust", arguments)

    def process(self):
        pass


class Gatling(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("Gatling", "gatling", arguments)

    def process(self):
        pass
