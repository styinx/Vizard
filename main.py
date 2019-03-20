from source.analyze import JMeter, Locust

if __name__ == "__main__":
    locust = Locust({
        "-f": "resource/Locust.py",
        "--no-web": "",
        "--only-summary": "",
        "-H": "www.example.com",
        "-P": "80",
        "-L": "CRITICAL",
        "-c": "10",
        "-t": "2s",
        "-r": "2"
    })
    locust.execute()

    jmeter = JMeter({
        "-n": "",
        "-t": "resource/JMeter.jmx",
        "": "",
        "-L": "jmeter.util=WARN"
    })
    jmeter.arg_separator = " "
    jmeter.execute("/home/chris/Programme/apache-jmeter-4.0/bin/")
