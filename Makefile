build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

shell:
	docker compose exec web python manage.py shell

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

createsuperuser:
	docker compose exec web python manage.py createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

test:
	docker compose exec web pytest

lint:
	docker compose exec web pylint --load-plugins pylint_django --django-settings-module=MyLearning.settings .

bash:
	docker compose exec web bash

dbshell:
	docker compose exec db psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-edX}

flush:
	docker compose down -v

.PHONY: build up down restart logs shell migrate makemigrations createsuperuser collectstatic test lint bash dbshell flush
