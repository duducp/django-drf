web: gunicorn project.asgi:application -k uvicorn.workers.UvicornWorker -e SIMPLE_SETTINGS=$SIMPLE_SETTINGS
release: SIMPLE_SETTINGS=$SIMPLE_SETTINGS python manage.py migrate --no-input
