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
        'headers': ['timeStamp', 'elapsed', 'responseCode', 'success', 'bytes',
                    'sentBytes', 'grpThreads', 'allThreads', 'Latency', 'IdleTime', 'Connect'],
        'metrics': {
            'elapsed time':     {
                'index': 1,
                'col':   'elapsed',
                'type':  'spline',
                'unit':  'ms'
            },
            'request status':           {
                'index': 3,
                'col':   'success',
                'type':  'pie',
                'unit':  ''
            },
            'received traffic': {
                'index': 4,
                'col':   'bytes',
                'type':  'column',
                'unit':  'bytes per request'
            },
            'sent traffic':     {
                'index': 5,
                'col':   'sentBytes',
                'type':  'column',
                'unit':  'bytes per request',
            },
            'latency':          {
                'index': 8,
                'col':   'Latency',
                'type':  'spline',
                'unit':  'ms'
            },
            'idle time':        {
                'index': 9,
                'col':   'IdleTime',
                'type':  'spline',
                'unit':  'ms'
            },
            'connection time':  {
                'index': 10,
                'col':   'Connect',
                'type':  'spline',
                'unit':  'ms'
            },
            # 'response time':    {
            #     'index': [1, 8, 9, 10],
            #     'col':   ['elapsed', 'Latency', 'IdleTime', 'Connect'],
            #     'type':  'spline',
            #     'unit':  'ms'
            # },
        }
    },
    'Locust': {
        'headers': ['timeStamp', 'service', 'type', 'success', 'responseTime', 'bytes'],
        'metrics': {
            # 'request status':        {
            #     'index': 2,
            #     'col': 'success',
            #     'type':  'pie',
            #     'unit':  ''
            # },
            'response time': {
                'index': 3,
                'col':   'responseTime',
                'type':  'spline',
                'unit':  'ms'
            },
            'sent traffic':  {
                'index': 4,
                'col':   'bytes',
                'type':  'column',
                'unit':  'bytes per request'
            },
        }
    }
}

# Activate Django-Heroku.
django_heroku.settings(locals())
