
all: down build up test post_test

build:
		docker compose build

up:
		docker compose up -d

down:
		docker compose down --remove-orphans

test:
		uv run -m pytest -s -vv --cov=src tests/

post_test:
		uv run coverage html

unit:
		uv run -m pytest -s -vv tests/unit

integration:
		uv run -m pytest -s -vv tests/integration

e2e:
		uv run -m pytest -s --v tests/e2e
