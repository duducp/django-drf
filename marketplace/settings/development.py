from .base import *  # noqa

DEBUG = True

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
}

EXTENSIONS_CONFIG['challenge']['host'] = os.getenv(
    'CHALLENGE_HOST', 'http://challenge-api.luizalabs.com'
)
