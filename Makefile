path_project=./marketplace
settings=marketplace.settings.dev

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
	pip install -U -r requirements/dev.txt

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


docker-run:
	docker-compose -f docker-compose.yml up -d --build

docker-down:
	docker-compose -f docker-compose.yml down -v

docker-migrate:
	docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput

docker-flush:
	docker-compose -f docker-compose.yml exec web python manage.py flush --noinput

docker-superuser:
	docker-compose -f docker-compose.yml exec web python manage.py createsuperuser

docker-shell:
	docker-compose -f docker-compose.yml exec web python manage.py shell -i ipython

docker-logs:
	docker-compose -f docker-compose.yml logs


run: collectstatic  ## run the django project
	gunicorn -b 0.0.0.0:8000 -t 300 marketplace.wsgi:application --reload

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

lint: ## run code lint
	isort .
	sort-requirements requirements/base.txt
	sort-requirements requirements/prod.txt
	sort-requirements requirements/dev.txt
	sort-requirements requirements/test.txt
	flake8 --show-source .
	pycodestyle --show-source .
	mypy marketplace/

safety-check: ## checks libraries safety
	safety check -r requirements/base.txt
	safety check -r requirements/prod.txt
	safety check -r requirements/dev.txt
	safety check -r requirements/test.txt

changelog-feature:  ## signifying a new feature
	@echo $(message) > changelog/$(filename).feature

changelog-bugfix:  ## signifying a bug fix
	@echo $(message) > changelog/$(filename).bugfix

changelog-doc:  ## signifying a documentation improvement
	@echo $(message) > changelog/$(filename).doc

changelog-removal:  ## signifying a deprecation or removal of public API
	@echo $(message) > changelog/$(filename).removal

changelog-misc:  ## a ticket has been closed, but it is not of interest to users
	@echo $(message) > changelog/$(filename).misc

release-draft: ## show new release changelog
	towncrier --draft

release-patch: ## create patch release (0.0.1)
	bumpversion patch --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bumpversion patch
	@echo 'To send the changes to the remote server run the make push command'

release-minor: ## create minor release (0.1.0)
	bumpversion minor --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bumpversion minor
	@echo 'To send the changes to the remote server run the make push command'

release-major: ## create major release (1.0.0)
	bumpversion major --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	git commit -am 'Update CHANGELOG'
	bumpversion major
	@echo 'To send the changes to the remote server run the make push command'

push:
	git push && git push --tags
