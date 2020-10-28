from .base import *  # noqa

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES['default'] = dj_database_url.parse(
    DATABASE_URL,
    engine='django-postgreconnect',
    conn_max_age=int(os.environ.get('DATABASES_CONN_MAX_AGE', '600')),
    ssl_require=True
)
