PYPATH=./src

install:
	poetry lock --no-update
	poetry install

migrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

seed-local:
	docker compose --env-file=.env -f docker/docker-compose.yaml exec bank-api poetry run python scripts/seeds.py

seed:
	poetry run python scripts/seeds.py

pre-commit:
	@poetry run pre-commit run --all-files

test:
	@poetry run pytest . -vv

test-coverage:
	@poetry run pytest -vv --cov-report=html --cov .

up:
	docker compose --env-file=.env -f docker/docker-compose.yaml up --build -d

down:
	docker compose --env-file=.env -f docker/docker-compose.yaml down
