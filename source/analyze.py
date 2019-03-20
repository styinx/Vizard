from source.util import Executable


class AnalyzeTool(Executable):
    def __init__(self, name, executable, arguments=None):
        super().__init__(executable, arguments)

        self.name = name

    def run(self, arguments=None):
        if arguments is not None:
            for arg in arguments:
                self.__setitem__(arg, arguments[arg])

        self.execute()


class JMeter(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("JMeter", "jmeter", arguments)


class Locust(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("Locust", "locust", arguments)


class Gatling(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__("Gatling", "gatling", arguments)
