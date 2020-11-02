from .base import *  # noqa

EXTENSIONS_CONFIG['challenge']['host'] = os.getenv(
    'CHALLENGE_HOST', 'http://challenge-api.luizalabs.com'
)
