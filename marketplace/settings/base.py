import os
import sys
from distutils.util import strtobool

import structlog as structlog

from marketplace.logging import processors

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
SECRET_KEY = os.getenv('SECRET_KEY', 'foo')
DEBUG = bool(strtobool(os.getenv('DEBUG', 'False')))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(';')
WSGI_APPLICATION = 'marketplace.wsgi.application'
ROOT_URLCONF = 'marketplace.urls'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'marketplace', 'static'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

CID_GENERATE = True
CID_CONCATENATE_IDS = True
CID_HEADER = 'X-Correlation-ID'
CID_RESPONSE_HEADER = 'X-Correlation-ID'

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'cid.apps.CidAppConfig',
]

LOCAL_APPS = [

]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cid.middleware.CidMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator',
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator',
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator',
        )
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'ignore_if_contains': {
            '()': 'marketplace.logging.filters.IgnoreIfContains',
            'substrings': ['/healthcheck', '/ping'],
        },
    },
    'formatters': {
        'json': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'filters': ['ignore_if_contains'],
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'marketplace': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['stdout'],
            'level': 'DEBUG'
        }
    }
}

structlog.configure(
    processors=[
        processors.hostname,
        processors.version,
        processors.correlation,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
