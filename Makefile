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

lint:
	cd backend && uv run ruff check .
	cd frontend && pnpm lint

format:
	cd backend && uv run ruff format .
	cd frontend && pnpm exec prettier --write .

test:
	cd backend && uv run pytest
	cd frontend && pnpm test
