# Marketplace

Project created with **Django** using the command `django-admin startproject marketplace .`

## Deploying application in production

To deploy to production the following environment variables must be defined:
```shell script
export SIMPLE_SETTINGS=marketplace.settings.production
export DJANGO_SETTINGS_MODULE=marketplace.settings.production
export SECRET_KEY=MY_SECRET_KEY
```

## Development mode

First, you must configure the virtual environment:
```shell script
python -m venv venv
```

After that activate virtualenv:
```shell script
source venv/bin/activate
```

Finally run the command to install the development dependencies:
```shell script
make dependencies
```
