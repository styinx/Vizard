#!/usr/bin/env python
import os
import sys
import time
import requests
import threading

from source.util import unpack_url_tar

from Vizard.settings import TOOL_PATH, CONF_JMETER, CONF_GATLING


def keep_alive():
    while True:
        time.sleep(60 * 5)  # sleep 5 minutes
        print('Send keep alive thread...', end='')
        print(requests.get('https://vizardous.herokuapp.com/'))


if __name__ == "__main__":
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vizard.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Couldn\'t import Django. Are you sure it\'s installed and '
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc

    if not os.path.exists(CONF_JMETER['executable_path']):
        print('Download JMeter...')
        unpack_url_tar(CONF_JMETER['download_url'], TOOL_PATH)

    # if not os.path.exists(CONF_GATLING['executable_path']):
    #     print('Download Gatling...')
    #     unpack_url_zip(CONF_GATLING['download_url'], TOOL_PATH)

    execute_from_command_line(sys.argv)
