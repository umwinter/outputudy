.PHONY: setup dev stop build ps logs lint format type-check test clean

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

# Run all tests in parallel
test:
	@echo "🧪 Running Backend Tests (Parallel)..."
	docker-compose exec backend pytest -n auto
	@echo "🧪 Running Frontend Tests..."
	docker-compose exec frontend pnpm test

# Clean up temporary files
	rm -rf frontend/node_modules

# Generate OpenAPI Client
api-gen:
	@echo "📜 Generating OpenAPI Schema..."
	@cd backend && DATABASE_URL="sqlite+aiosqlite:///:memory:" SECRET_KEY="gen-secret" /Users/umeta/.local/bin/uv run python -c "from app.main import app; import json; print(json.dumps(app.openapi()))" > ../frontend/src/types/openapi.json
	@echo "🔧 Generating TypeScript Client..."
	@cd frontend && npx -y openapi-typescript-codegen --input src/types/openapi.json --output src/lib/api-client --client fetch
	@echo "✅ Done!"
