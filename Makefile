run:
	python manage.py runserver 0.0.0.0:8000

app:
	python manage.py startapp $(name)

migrate:
	python manage.py migrate

migration:
	python manage.py makemigrations

migration-empty:
	python manage.py makemigrations --empty $(app)

create-superuser:
	python manage.py createsuperuser
