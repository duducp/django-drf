import os
import sys
from datetime import timedelta
from distutils.util import strtobool

from django.urls import reverse_lazy

import dj_database_url
import structlog as structlog

from marketplace.logging import processors

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
SECRET_KEY = os.getenv('SECRET_KEY', 'foo')
DEBUG = bool(strtobool(os.getenv('DEBUG', 'False')))

WSGI_APPLICATION = 'marketplace.wsgi.application'
ROOT_URLCONF = 'marketplace.urls'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(';')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
LOCALE_PATHS = [os.path.join(BASE_DIR, 'marketplace', 'locales')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'marketplace', 'statics')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'medias')
MEDIA_URL = '/medias/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/statics/'

TIME_ZONE = 'UTC'
USE_TZ = True
USE_L10N = True
USE_I18N = False
LANGUAGE_CODE = 'en-us'

CID_GENERATE = True
CID_CONCATENATE_IDS = True
CID_HEADER = 'X-Correlation-ID'
CID_RESPONSE_HEADER = 'X-Correlation-ID'

LOGIN_URL = reverse_lazy('admin:login')
LOGOUT_URL = reverse_lazy('admin:logout')

SESSION_EXPIRE_SECONDS = int(os.getenv('SESSION_EXPIRE_SECONDS', '3600'))
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = 'login/'

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
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'rest_framework_filters',
    'rest_framework_simplejwt.token_blacklist',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.psutil',
]

LOCAL_APPS = [
    'marketplace.apps.clients',
    'marketplace.apps.favorites',
    'marketplace.apps.ping',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DEFAULT_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

THIRD_PARTY_MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'cid.middleware.CidMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

LOCAL_MIDDLEWARE = [
    'marketplace.middlewares.version_header.VersionHeaderMiddleware',
]

MIDDLEWARE = DEFAULT_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + LOCAL_MIDDLEWARE

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'marketplace', 'templates'),
        ],
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

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgres://postgres:postgres@127.0.0.1:5432/postgres'
)

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        engine='django-postgreconnect',
        conn_max_age=int(
            os.environ.get('DATABASE_DEFAULT_CONN_MAX_AGE', '600')
        ),
        ssl_require=bool(
            strtobool(
                os.getenv('DATABASE_DEFAULT_SSL_REQUIRE', 'True')
            )
        )
    )
}

REDIS_URL = os.environ.get(
    'REDIS_URL',
    'redis://127.0.0.1:6379/1'
).split(';')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'KEY_PREFIX': 'django',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
            'CONNECTION_POOL_KWARGS': {
                'retry_on_timeout': True
            }
        }
    },
}

CACHES_TTL = {
    'product': int(os.environ.get('CACHE_TTL_PRODUCT', '10800'))
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # noqa
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # noqa
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # noqa
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # noqa
]

REST_FRAMEWORK = {
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
    'DEFAULT_VERSIONING_CLASS': (
        'rest_framework.versioning.NamespaceVersioning'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework_xml.parsers.XMLParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.environ.get('THROTTLE_RATES_ANON', '50/second'),
    },
    'EXCEPTION_HANDLER': 'marketplace.exceptions.custom_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'rest_framework_filters.backends.RestFrameworkFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # noqa
    'PAGE_SIZE': 20,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

APPLICATION = {
    'name': 'Marketplace',
    'description': '',
    'terms_of_service': '',
    'contact': {
        'name': 'Carlos Eduardo',
        'email': 'duducp2013@gmail.com',
        'url': ''
    },
    'doc_public': bool(strtobool(os.getenv('APPLICATION_DOC_PUBLIC', 'True')))
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.InlineSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.JSONFieldInspector',
        'drf_yasg.inspectors.HiddenFieldInspector',
        'drf_yasg.inspectors.RecursiveFieldInspector',
        'drf_yasg.inspectors.SerializerMethodFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ],
    'DOC_EXPANSION': 'list',
    'USE_SESSION_AUTH': True
}

DRF_YASG_EXCLUDE_VIEWS = []

HEALTH_CHECK = {
    'DISK_USAGE_MAX': int(
        os.getenv('HEALTH_CHECK_DISK_USAGE_MAX', '90')
    ),  # percent
    'MEMORY_MIN': int(
        os.getenv('HEALTH_CHECK_MEMORY_MIN', '100')
    ),  # in MB
}

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

EXTENSIONS_CONFIG = {
    'challenge': {
        'timeout': float(os.getenv('CHALLENGE_TIMEOUT', '2')),
        'host': os.getenv('CHALLENGE_HOST', 'http://localhost'),
        'routes': {
            'product': os.getenv(
                'CHALLENGE_ROUTE_PRODUCT',
                '/api/product/{product_id}/'
            ),
        },
    }
}
