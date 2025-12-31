.PHONY: help up down build logs backend-shell test-backend test-frontend lint format

help:
	@echo "Available commands:"
	@echo "  make up            - Start all services (detached)"
	@echo "  make down          - Stop and remove containers"
	@echo "  make build         - Build/Rebuild services"
	@echo "  make logs          - Tail logs for all services"
	@echo "  make backend-shell - Enter backend container shell"
	@echo "  make test-backend  - Run backend tests"
	@echo "  make test-frontend - Run frontend tests"
	@echo "  make lint          - Run linting (ruff, eslint)"
	@echo "  make format        - Run formatting (ruff, prettier)"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up -d --build

logs:
	docker-compose logs -f

backend-shell:
	docker-compose exec backend /bin/bash

test-backend:
	docker-compose run --rm backend pytest

test-frontend:
	docker-compose run --rm frontend pnpm test

lint:
	docker-compose run --rm backend ruff check .
	# Frontend linting might require pnpm run lint inside container or locally if node is installed
	# docker-compose run --rm frontend pnpm lint

format:
	docker-compose run --rm backend ruff format .
	# docker-compose run --rm frontend pnpm format
