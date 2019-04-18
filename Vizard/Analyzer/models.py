import json
import pickle
from source.util import Executable


class Vizardplan:
    def __init__(self, target, configuration):
        open(target, "w").write(json.dumps(configuration))


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

    def process(self, path=None):
        pass


class JMeter(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("JMeter", "jmeter", arguments)

    def process(self, path=None):
        result = {}
        result_file = "result.json"

        if path is not None:
            result_file = path
            f = open(result_file, "r")

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

        open(result_file[:result_file.rfind(".")] + "_processed.json", "w").write(json.dumps(result))
        pickle.dump(result, open(result_file[:result_file.rfind(".")] + "_cached.json", "wb"))


class Locust(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("Locust", "locust", arguments)

    def process(self, path=None):
        pass


class Gatling(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("Gatling", "gatling", arguments)

    def process(self, path=None):
        pass
