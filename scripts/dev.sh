#!/usr/bin/env bash
set -euo pipefail

echo "Starting infra..."
docker compose up -d postgres redis minio

echo "Backend: cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000"
echo "Frontend: cd frontend && pnpm dev"
