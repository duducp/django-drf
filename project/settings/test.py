from .base import *  # noqa

DATABASES['default'] = dj_database_url.parse('sqlite://:memory:')

CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}
CACHES['concurrent'] = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}
