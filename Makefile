path_project=./marketplace
settings=marketplace.settings.development

ifdef SIMPLE_SETTINGS
	settings=$(SIMPLE_SETTINGS)
else
	export SIMPLE_SETTINGS=$(settings)
endif

export DJANGO_SETTINGS_MODULE=$(settings)


clean: ## clean local environment
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log

dependencies: ## install development dependencies
	pip install -U -r requirements/development.txt

superuser: ## creates superuser for admin
	python manage.py createsuperuser

collectstatic: ## creates static files for admin
	python manage.py collectstatic

app:  ## creates a new django application Ex.: make app name=products
	cd $(path_project) && python ../manage.py startapp $(name)

	@echo "# Create your exceptions here." > $(path_project)/$(name)/exceptions.py
	cd $(path_project)/$(name) && mkdir -p tests
	@echo > $(path_project)/$(name)/tests/__init__.py
	rm $(path_project)/$(name)/tests.py


run:  ## run the django project
	python manage.py runserver 0.0.0.0:8000

migrate:  ## apply migrations to the database
	python manage.py migrate

migration:  ## creates migration file according to the models
	python manage.py makemigrations

migration-empty:  ## creates blank migration file
	python manage.py makemigrations --empty $(app)

migration-detect:  ## detect missing migrations
	python manage.py makemigrations --dry-run --noinput | grep 'No changes detected' -q || (echo 'Missing migration detected!' && exit 1)

shell:
	@echo 'Loading shell with settings = $(settings)'
	python manage.py shell -i ipython

test: clean ## run tests
	pytest -x

test-matching: clean ## run matching tests
	pytest -x -k $(q) --pdb

test-debug: clean ## run tests with pdb
	pytest -x --pdb

test-coverage: clean ## run tests with coverage
	pytest -x --cov=ecommerce/ --cov-report=term-missing --cov-report=xml

test-coverage-html: clean ## run tests with coverage with html report
	pytest -x --cov=ecommerce/ --cov-report=html:htmlcov

test-coverage-html-server: ## run server for view coverage tests
	cd htmlcov && python -m http.server 8001 --bind 0.0.0.0
