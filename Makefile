# Django 

.PHONY:django-shell
django-shell:
	docker-compose -f local.yml run --rm api python -m core.manage shell

.PHONY:dbshell
dbshell:
	docker-compose -f local.yml exec postgres psql --username=medium --dbname=medium

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
	docker-compose -f local.yml run --rm api python -m core.manage create_default_admin


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

.PHONY:test-d
test-d:
	docker-compose exec app make test-r


# Docker

.PHONY:local-project-up
local-project-up:
	docker-compose -f local.yml up --build -d --remove-orphans

.PHONY:local-project-down
local-project-down:
	docker-compose -f local.yml down

.PHONY:down-v
down-v:
	docker-compose -f local.yml down -v

.PHONY:local-db-backup
local-db-backup:
	docker-compose -f local.yml exec postgres backup

.PHONY:local-backup-list
local-backup-list:
	docker-compose -f local.yml exec postgres backups

.PHONY:local-db-restore
local-db-restore:
	docker-compose -f local.yml exec postgres restore $(F)

.PHONY:volume
volume:
	docker volume inspect medium_local_postgres_db

.PHONY:docker-logs
docker-logs:
	docker-compose -f local.yml logs


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

.PHONY:update
update: install migrate update-precommit ;



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
