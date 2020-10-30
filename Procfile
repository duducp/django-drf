web: gunicorn marketplace.asgi:application -k uvicorn.workers.UvicornWorker -e SIMPLE_SETTINGS=$SIMPLE_SETTINGS -e DJANGO_SETTINGS_MODULE=$SIMPLE_SETTINGS
release: SIMPLE_SETTINGS=$SIMPLE_SETTINGS DJANGO_SETTINGS_MODULE=$SIMPLE_SETTINGS python manage.py migrate --no-input
