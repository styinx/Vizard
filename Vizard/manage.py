#!/usr/bin/env python
import os
import sys
import io
import tarfile
import urllib.request

from Vizard.settings import JMETER_URL

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vizard.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    archive = tarfile.open(fileobj=io.BytesIO(urllib.request.urlopen(JMETER_URL).read()))
    archive.extractall("./resource/")
    archive.close()

    execute_from_command_line(sys.argv)
