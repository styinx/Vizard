import os
import psutil
import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ha&qfp@hgs!0kar@ngb*z9=g*v2vjc(j)bdln!dtwxo6oh4hsb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Analyzer.apps.AnalyzerConfig',
    'Presenter.apps.PresenterConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Vizard.urls'

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     ['templates', 'Vizard/templates'],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Vizard.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

DATE_FORMAT = '%H:%M:%S %d/%m/%Y'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

RESOURCE_PATH = BASE_DIR + '/resource'
TOOL_PATH = RESOURCE_PATH + '/tools'
TEMPLATE_PATH = RESOURCE_PATH + '/templates'
USER_PATH = RESOURCE_PATH + '/users'
TASK_PATH = RESOURCE_PATH + '/tasks'

MAX_THREADS = psutil.cpu_count()

RESPONSE = {
    'status':  200,
    'message': ''
}

ERROR = {
    '200': 'All good.',
    '400': '',
    '404': '',
    '501': 'We are sorry, this feature is currently not implemented.'
}

JMETER_VERSION = 'apache-jmeter-5.1.1'
CONF_JMETER = {
    'path':            TOOL_PATH + '/' + JMETER_VERSION,
    'executable_path': TOOL_PATH + '/' + JMETER_VERSION + '/bin/',
    'template':        TEMPLATE_PATH + '/JMeter_template.jmx',
    'download_url':    'https://www-eu.apache.org/dist/jmeter/binaries/' + JMETER_VERSION + '.tgz'
}

CONF_LOCUST = {
    # executable is installed via pip
    'template': TEMPLATE_PATH + '/Locust_template.py',
}

GATLING_VERSION = 'gatling-charts-highcharts-bundle-3.1.2'
CONF_GATLING = {
    'path':            TOOL_PATH + '/' + GATLING_VERSION,
    'executable_path': TOOL_PATH + '/' + GATLING_VERSION + '/bin/',
    'template':        TEMPLATE_PATH + '/Gatling_template.py',
    'download_url':    'https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/3.1.2/gatling-charts-highcharts-bundle-3.1.2-bundle.zip'
}

REPORT = {
    'JMeter': {
        'wiki':    'Apache_JMeter',
        'link':    'https://jmeter.apache.org/',
        'headers': ['timeStamp', 'elapsed', 'responseCode', 'success', 'bytes',
                    'sentBytes', 'grpThreads', 'allThreads', 'Latency', 'IdleTime', 'Connect'],
        'metrics': {
            'elapsed time':     {
                'index':      1,
                'dtype':      int,
                'col':        'elapsed',
                'type':       'spline',
                'unit':       'ms',
                'definition': str(
                    'The elapsed time is the amount of time it takes to send the first request '
                    'until the last response is received. This metric does not include the time '
                    'a client is executing code.')
            },
            'request status':   {
                'index':      3,
                'dtype':      bool,
                'col':        'success',
                'type':       'gauge',
                'unit':       '',
                'definition': str(
                    'If a request does not reach the server or is refused by it, the request was not '
                    'successful. An unsuccessful request can contain the reason of the refusal as plain '
                    'text in the response text. Another reason is a faulty connection to the server.')
            },
            'server status':    {
                'index':      3,
                'dtype':      bool,
                'col':        'success',
                'type':       'statusline',
                'unit':       '',
                'definition': str(
                    'If a request does not reach the server or is refused by it, the request was not '
                    'successful. An unsuccessful request can contain the reason of the refusal as plain '
                    'text in the response text. Another reason is a faulty connection to the server.')
            },
            'received traffic': {
                'index':      4,
                'dtype':      int,
                'col':        'bytes',
                'type':       'column',
                'unit':       'bytes per request',
                'definition': str(
                    'To perform a request, it is necessary to exchange data between client and '
                    'server. This data consists of header data and meta information, which is '
                    'needed by the server. The amount of exchanged information is measured in bytes.')
            },
            # 'sent traffic':     {
            #     'index':      5,
            #     'dtype':      int,
            #     'col':        'sentBytes',
            #     'type':       'column',
            #     'unit':       'bytes per request',
            #     'definition': str()
            # },
            'latency':          {
                'index':      8,
                'dtype':      int,
                'col':        'Latency',
                'type':       'spline',
                'unit':       'ms',
                'definition': str(
                    'Latency is the amount of time a message takes to traverse a system. '
                    'In a computer network, it is an expression of how much time it takes for '
                    'a packet of data to get from one designated point to another. '
                    'It is measured as the time required for a request to be sent to the '
                    'server and returned to its sender. '
                    'Latency depends on the speed of the transmission medium  and the delays '
                    'in the transmission by devices along the way. ' +
                    'A low latency indicates a high network efficiency.')
            },
            # 'idle time':        {
            #     'index':      9,
            #     'dtype':      int,
            #     'col':        'IdleTime',
            #     'type':       'spline',
            #     'unit':       'ms',
            #     'definition': str()
            # },
            'connection time':  {
                'index':      10,
                'dtype':      int,
                'col':        'Connect',
                'type':       'spline',
                'unit':       'ms',
                'definition': str(
                    'The connection time is the amount of time it takes to establish a connection '
                    'between a client and the server. If the connection request between client and '
                    'server was successful, the client can send further requests. If the connection '
                    'was not successful, no further requests can be send to the server. The connection '
                    'time is also part of the latency. ')
            },
            'response time':    {
                'dtype':      int,
                'index':      [1, 8, 9, 10],
                'col':        ['elapsed', 'Latency', 'IdleTime', 'Connect'],
                'type':       'spline',
                'unit':       'ms',
                'definition': str(
                    'Response time is the total amount of time it takes to respond to a request for '
                    'service. That service can be anything from a memory fetch, to a disk IO, to a '
                    'complex database query, or loading a full web page. The response time is the sum '
                    'of the service time and wait time. The service time is the time it takes to do '
                    'the work you requested. For a given request the service time varies little as '
                    'the workload increases – to do X amount of work it always takes X amount of '
                    'time. The wait time is how long the request had to wait in a queue before being '
                    'serviced and it varies from zero, to a large multiple of the service time.')
            }
        }
    },
    'Locust': {
        'wiki':    '',
        'link':    'https://locust.io/',
        'headers': ['timeStamp', 'service', 'type', 'success', 'responseTime', 'bytes'],
        'metrics': {
            'request status': {
                'index':      2,
                'dtype':      bool,
                'col':        'success',
                'type':       'gauge',
                'unit':       '',
                'definition': str(
                    'If a request does not reach the server or is refused by it, the request was not '
                    'successful. An unsuccessful request can contain the reason of the refusal as plain '
                    'text in the response text. Another reason is a faulty connection to the server.')
            },
            'server status': {
                'index':      3,
                'dtype':      bool,
                'col':        'success',
                'type':       'statusline',
                'unit':       '',
                'definition': str(
                    'If a request does not reach the server or is refused by it, the request was not '
                    'successful. An unsuccessful request can contain the reason of the refusal as plain '
                    'text in the response text. Another reason is a faulty connection to the server.')
            },
            'response time':  {
                'index':      3,
                'dtype':      float,
                'col':        'responseTime',
                'type':       'spline',
                'unit':       'ms',
                'definition': str(
                    'Response time is the total amount of time it takes to respond to a request for '
                    'service. That service can be anything from a memory fetch, to a disk IO, to a '
                    'complex database query, or loading a full web page. The response time is the sum '
                    'of the service time and wait time. The service time is the time it takes to do '
                    'the work you requested. For a given request the service time varies little as '
                    'the workload increases – to do X amount of work it always takes X amount of '
                    'time. The wait time is how long the request had to wait in a queue before being '
                    'serviced and it varies from zero, to a large multiple of the service time.')
            },
            'sent traffic':   {
                'index':      4,
                'dtype':      float,
                'col':        'bytes',
                'type':       'column',
                'unit':       'bytes per request',
                'definition': str()
            },
        }
    }
}

VALUES = {
    '0':  'Offline',
    '1':  'Online',
    'True':  'successful',
    'False': 'not successful',
}

# Activate Django-Heroku.
django_heroku.settings(locals())
