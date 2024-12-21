# Django 

.PHONY:django-shell
django-shell:
	docker-compose -f local.yml run --rm api python -m core.manage shell


.PHONY:migrations
migrations:
	docker-compose -f local.yml run --rm api python -m core.manage makemigrations

.PHONY:show-migrations
show-migrations:
	docker-compose -f local.yml run --rm api python -m core.manage showmigrations --plan


.PHONY:migrate
migrate:
	docker-compose -f local.yml run --rm api python -m core.manage migrate

.PHONY:statics
statics:
	docker-compose -f local.yml run --rm api python -m core.manage collectstatics --no-input --clear

.PHONY:sever
server:
	poetry run python -m core.manage runserver

.PHONY:admin
admin:
	docker-compose -f local.yml run --rm api python -m core.manage shell \
	-c "from django.contrib.auth import get_user_model; \
    User = get_user_model(); \
	email = 'admin@example.com'; \
	password = 'admin'; \
	first_name = 'test'; \
	last_name = 'test'; \
    User.objects.create_superuser(email=email, password=password, first_name=first_name, last_name=last_name) \
    if not User.objects.filter(email='admin@example.com').exists() \
    else print('Superuser already exists')"


# Test

.PHONY:test
test:
	@RUNNING_MODE=test \
	poetry run pytest $(ARGS)

.PHONY:test-lf
test-lf:
	@RUNNING_MODE=test \
	poetry run pytest -v -rs --lf

.PHONY:test-r
test-r:
	@RUNNING_MODE=test \
	poetry run pytest -v -rs -n auto --show-capture=no --cache-clear \
	--cov=core --cov-report term-missing --cov-report html --cov-config=pyproject.toml



# Services

.PHONY:local-project-up
local-project-up:
	docker-compose -f local.yml up --build -d --remove-orphans

.PHONY:local-project-down
local-project-down:
	docker-compose -f local.yml down

.PHONY:down-v
down-v:
	docker-compose -f local.yml down -v



.PHONY:volume
volume:
	docker volume inspect medium_local_postgres_db

.PHONY:docker-logs
docker-logs:
	docker-compose -f local.yml logs


# Image
img-prune:
	./run prune-all-images -f


# Precommit
.PHONY:lint
lint:
	git add .; poetry run pre-commit run --all-files

.PHONY:update-precommit
update-precommit:
	poetry run pre-commit uninstall; poetry run pre-commit clean; poetry run pre-commit install


# Commit
.PHONY:commit
commit:
	poetry run cz commit

.PHONY:bump
bump:
	poetry run cz bump



# Interact with db

.PHONY:load-fixtures
load-fixtures:
	poetry run python -m core.manage load_fixtures

.PHONY:extract-db
extract-db:
	poetry run python -m core.manage dumpdata > core/product/fixtures/fixtures.json

.PHONY:dump-models
dump-models:
	poetry run python -m core.manage dump_models

.PHONY:local-db-backup
local-db-backup:
	docker-compose -f local.yml exec postgres backup

.PHONY:local-backup-list
local-backup-list:
	docker-compose -f local.yml exec postgres backups

.PHONY:local-db-restore
local-db-restore:
	docker-compose -f local.yml exec postgres restore $(F)


# Container
.PHONY:shell-api
shell-api:
	docker exec -it api bash

.PHONY:shell-db
shell-db:
	docker-compose -f local.yml exec postgres psql --username=medium --dbname=medium


.PHONY:log-api
log-api:
	docker logs medium-api-1

.PHONY:log-db
log-db:
	docker logs medium-postgres-1
