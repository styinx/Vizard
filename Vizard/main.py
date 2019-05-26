from Analyzer.tools import JMeter
from time import time

if __name__ == "__main__":

    jmeter = JMeter({
        "-n": "",
        "-t": "resource/JMeter.jmx",
        "-l": "result" + str(time()) + ".csv",
        "-L": "jmeter.util=WARN"
    })
    jmeter.arg_separator = " "
    jmeter.execute("./resource/apache-jmeter-5.1.1/bin/")
