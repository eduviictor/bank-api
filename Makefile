# install-pyenv:
# 	@command -v pyenv >/dev/null 2>&1 || curl https://pyenv.run | bash

# setup-project:install-pyenv
# 	pyenv versions | grep 3.12.0 || pyenv install 3.12.0
# 	pyenv local 3.12.0
# 	python --version
# 	python -m venv venv
# 	. venv/bin/activate
# 	pip install --upgrade pip
# 	pip install poetry
# 	poetry install --only dev --no-root

install:
	. venv/bin/activate
	poetry lock --no-update
	poetry install

migrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

seed:
	docker compose --env-file=.env -f docker/docker-compose.yaml exec bank-api poetry run python scripts/seeds.py

pre-commit:
	@poetry run pre-commit run --all-files

tests:
	@echo "Running tests"
	@poetry run pytest --disable-warnings -vv --cov-report=html --cov .

up:
	docker compose --env-file=.env -f docker/docker-compose.yaml up --build -d
