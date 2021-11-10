help:
	@echo "help  -- print this help"
	@echo "start -- start docker stack"
	@echo "stop  -- stop docker stack"
	@echo "ps    -- show status"
	@echo "clean -- clean all artifacts"
	@echo "test  -- run tests using docker"
	@echo "dockershell -- run bash inside docker"
	@echo "shell_plus -- run django shell_plus inside docker"
	@echo "bootstrap --build containers, run django migrations, load fixtures and create the a superuser"

start:
	docker build -t pyarweb .
	docker-compose up

stop:
	docker-compose stop

ps:
	docker-compose ps

clean: stop
	docker-compose rm --force -v

only_test:
	docker-compose run --rm web python3 ./manage.py test  -v2 --noinput

pep8:
	docker-compose run --rm web flake8

test: pep8 only_test

dockershell:
	docker-compose run --rm web /bin/bash

migrations:
	docker-compose run --rm web python3 manage.py makemigrations

migrate:
	docker-compose run --rm web python3 manage.py migrate --skip-checks

shell_plus:
	docker-compose run --rm web python3 manage.py shell_plus

.PHONY: help start stop ps clean test dockershell shell_plus only_test pep8
