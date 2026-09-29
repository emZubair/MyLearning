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

upgrade:
	docker compose run --rm --no-deps web sh -c '\
		pip install --upgrade $$(sed -e "s/[=<>~!].*//" -e "/^\s*#/d" -e "/^\s*$$/d" requirements.txt) && \
		python -c "import re, importlib.metadata as md; \
names = [re.split(r\"[=<>~! ]\", l)[0] for l in open(\"requirements.txt\").read().splitlines() if l.strip() and not l.startswith(\"#\")]; \
open(\"requirements.txt\", \"w\").write(\"\".join(f\"{n}=={md.version(n)}\n\" for n in names))"'
	git diff --stat requirements.txt

pr:
	@set -eu; \
	branch="$$(git symbolic-ref --quiet --short HEAD)" || { echo "Error: detached HEAD" >&2; exit 1; }; \
	[ "$$branch" != "main" ] || { echo "Error: cannot create a PR from main" >&2; exit 1; }; \
	[ -z "$$(git status --porcelain)" ] || { echo "Error: commit or stash your changes first" >&2; exit 1; }; \
	command -v gh >/dev/null || { echo "Error: GitHub CLI (gh) is required" >&2; exit 1; }; \
	git fetch origin main:main; \
	git rebase main; \
	git push --force-with-lease --set-upstream origin "$$branch"; \
	title="$$(git log -1 --pretty=%s)"; \
	body="### $$(git log -1 --pretty=%B)"; \
	gh pr create --base main --head "$$branch" --title "$$title" --body "$$body"

.PHONY: build up down restart logs shell migrate makemigrations createsuperuser collectstatic test lint bash dbshell flush upgrade pr
