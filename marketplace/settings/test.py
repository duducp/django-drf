from .base import *  # noqa

DATABASE_URL = 'sqlite://:memory:'
DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}
