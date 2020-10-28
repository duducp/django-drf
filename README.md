# Marketplace

Project created with **Django** using the command `django-admin startproject marketplace .`

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

To access the admin it is necessary to create the superuser. This can be done
with the following command:

```shell script
make superuser
```

## Deploying application in production

To deploy to production the following environment variables must be defined:
```shell script
export SIMPLE_SETTINGS=marketplace.settings.prod
export DJANGO_SETTINGS_MODULE=marketplace.settings.prod
export SECRET_KEY="your_key_here"
export DATABASE_URL="sqlite:///db.sqlite3"
```

Optionals:
```shell script
export ALLOWED_HOSTS="*;"
```

### Deploying on Heroku
I am assuming that you already know [Heroku](https://dashboard.heroku.com/apps)
and that you have already installed the CLI and logged in.

The first thing to do is to create the app on Heroku and this can be done with
the command `heroku create <name-app>`. After creating the app, the CLI itself
will add _git remote_ to you in your Django project.

The next step is to send your project to Heroku with the command
`git push heroku master -f`.

Now it's time to set the environment variables in Heroku:
```shell script
heroku config:set DEBUG="False"
heroku config:set SIMPLE_SETTINGS=marketplace.settings.prod
heroku config:set DJANGO_SETTINGS_MODULE=marketplace.settings.prod
heroku config:set SECRET_KEY="your_key_here"
```

To configure the [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql)
database, simply run the command `heroku addons:create heroku-postgresql:hobby-dev`.

To configure the [Redis](https://elements.heroku.com/addons/heroku-redis)
database, simply run the command `heroku addons:create heroku-redis:hobby-dev`.

By running the two commands above, Heroku will create two environment variables
called DATABASE_URL and REDIS_URL.

With the database configured, we can run migrations with the command
`heroku run make migrate`.

The last step is to create the super user for Django Admin:
```shell script
heroku run bash
make superuser
```

The first command we are accessing Heroku's bash and the second we are using to
create the super user.

Others commands:
- **heroku config** view the application's environment variables
- **heroku logs** view the latest application logs
- **heroku addons** view installed addons
- **heroku addons:open <name_addon>** opens the panel for a particular addon
- **heroku pg:psql** open the postgres shell
- **heroku redis:cli** open the redis shell

Note:

Heroku looks at the file **Procfile** in order to detect the
applications that should be run. It automatically identifies that it is a
Django application and runs some commands during application startup, as well
as **collectfiles**. In this file there is a **release** command, it will be
executed after the application initialization and it is not a specific
application. The **runtime.txt** file is used to specify the version of python
that Heroku should use.
