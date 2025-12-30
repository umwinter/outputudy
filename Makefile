.PHONY: setup dev stop build ps logs lint format type-check clean

# Default target
all: dev

# Initialize environment
setup:
	bash scripts/setup.sh

# Start containers
dev:
	docker-compose up -d

# Stop containers
stop:
	docker-compose stop

# Build containers
build:
	docker-compose build

# Check container status
ps:
	docker-compose ps

# Show logs
logs:
	docker-compose logs -f

# Run all lint checks
lint:
	@echo "🔍 Running Backend Lint (Ruff)..."
	docker-compose exec backend ruff check .
	@echo "🔍 Running Frontend Lint (ESLint)..."
	docker-compose exec frontend pnpm lint

# Run all formatters
format:
	@echo "🎨 Formatting Backend (Ruff)..."
	docker-compose exec backend ruff format .
	@echo "🎨 Formatting Frontend (Prettier)..."
	docker-compose exec frontend pnpm format

# Run all type checks
type-check:
	@echo "⌨️ Checking Backend Types (MyPy)..."
	docker-compose exec backend mypy .
	@echo "⌨️ Checking Frontend Types (TSC)..."
	docker-compose exec frontend pnpm type-check

# Clean up temporary files
clean:
	rm -rf backend/.mypy_cache
	rm -rf backend/.ruff_cache
	rm -rf frontend/.next
	rm -rf frontend/node_modules
