.PHONY: up down logs build ps restart backend-shell frontend-shell migrate lint format test

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

ps:
	docker compose ps

restart:
	docker compose restart

backend-shell:
	docker compose exec backend bash

frontend-shell:
	docker compose exec frontend sh

migrate:
	docker compose exec backend uv run alembic upgrade head

# lint/format/test all run inside the containers (like `migrate` does) rather than on the
# host — that way they work with just Docker running, no native uv/pnpm install required, and
# the backend targets automatically use the right DATABASE_URL for the Compose Postgres.
# Requires `make up` (or `make up -d`) to already be running.
lint:
	docker compose exec backend uv run ruff check .
	docker compose exec frontend pnpm lint

format:
	docker compose exec backend uv run ruff format .
	docker compose exec frontend pnpm exec prettier --write .

test:
	docker compose exec backend uv run pytest
	docker compose exec frontend pnpm test
