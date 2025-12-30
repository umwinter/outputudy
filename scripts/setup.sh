#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting development environment setup..."

# 1. Check dependencies
echo "🔍 Checking dependencies..."
command -v docker >/dev/null 2>&1 || { echo >&2 "❌ Docker is not installed. Please install it first."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo >&2 "❌ docker-compose is not installed. Please install it first."; exit 1; }
command -v pre-commit >/dev/null 2>&1 || { echo >&2 "⚠️ pre-commit is not installed locally. Some hooks might not install correctly."; }

# 2. Environment variables
if [ ! -f .env ]; then
    echo "📄 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please review and update if necessary."
else
    echo "✅ .env already exists."
fi

# 3. Git Hooks
echo "🪝 Installing Git Hooks..."
if command -v pre-commit >/dev/null 2>&1; then
    pre-commit install
    pre-commit install --hook-type pre-push
    echo "✅ Git Hooks installed."
else
    echo "⚠️ Skipping Git Hook installation (pre-commit not found)."
fi

# 4. Docker containers
echo "🐳 Building and starting Docker containers..."
docker-compose up -d --build

# 5. Database Initialization
echo "🗄️ Waiting for database to be ready..."
# Simple wait loop for the database
sleep 5

echo "🚜 Running database migrations..."
docker-compose exec backend alembic upgrade head

echo "🌱 Seeding initial data..."
docker-compose exec backend sh -c "PYTHONPATH=. python scripts/seed.py"

echo "✨ Setup complete! You can now access:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Adminer: http://localhost:8080"
