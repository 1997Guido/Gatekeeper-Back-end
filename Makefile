clean:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

install:
	pip install -r requirements/base.txt
	pip install -r requirements/local.txt

lint:
	flake8 gatekeeper
	isort --check-only --diff gatekeeper
	djlint ./gatekeeper/templates

pre-commit:
	pre-commit run --all-files

account:
	DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --no-input --email admin@example.com --username admin

format:
	black gatekeeper
	isort gatekeeper
	djlint --reformat ./gatekeeper/templates

makemessages:
	python manage.py makemessages --all

compilemessages:
	python manage.py compilemessages

static-files:
	rm -rf gatekeeper/public/static
	yarn build
	manage.py collectstatic --noinput

start:
	python manage.py runserver

frontend:
	npm run dev
