from Analyzer.processing import AnalysisData
from Vizard.settings import REPORT

from source.util import Executable, serialize, write, read, dump, normalize_value


# Stores config values for the experiment to restore them to the report.
class Vizardplan:
    def __init__(self, task, configuration):
        write(dump(configuration), task.path + '/vizard.json')


# Stores the experiment file from a template filled with configuration values.
class Testplan:
    def __init__(self, template, target, arguments):
        self.target = target
        self.content = open(template, 'r').read()
        self.configuration = self.content

        for key, value in arguments.items():
            self.configuration = self.configuration.replace(key, value)

        write(self.configuration, target)


# Base for every analysis tool.
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
        super().__init__('JMeter', 'jmeter', arguments)

    def process(self, path=None):
        result_file = path
        file_prefix = result_file[:result_file.rfind('.')]

        headers = REPORT['JMeter']['headers']
        headers = {i: x for i, x in enumerate(headers)}
        serialize(AnalysisData(result_file, headers), file_prefix + '_cached.dat')


class Locust(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__('Locust', 'locust', arguments)

    def process(self, path=None):
        result_file = path
        file_prefix = result_file[:result_file.rfind('.')]

        headers = REPORT['Locust']['headers']
        headers = {i: x for i, x in enumerate(headers)}
        serialize(AnalysisData(result_file, headers), file_prefix + '_cached.dat')


class Gatling(AnalyzeTool):
    def __init__(self, arguments=None):
        super().__init__('Gatling', 'gatling', arguments)

    def process(self, path=None):
        pass
