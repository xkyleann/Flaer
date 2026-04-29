#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND="$ROOT/flaer/backend"
FRONTEND="$ROOT/flaer/frontend-svelte"

# ── Backend ──────────────────────────────────────────────
if [ ! -f "$BACKEND/.env" ]; then
  echo "Creating .env from .env.example..."
  cp "$BACKEND/.env.example" "$BACKEND/.env"
  JWT=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  sed -i '' "s/your-secret-key-here-change-in-production/$JWT/" "$BACKEND/.env"
fi

cd "$BACKEND"
venv/bin/python init_database.py --quiet 2>/dev/null || true
venv/bin/uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo "Backend started (PID $BACKEND_PID) → http://localhost:8000"

# ── Frontend ─────────────────────────────────────────────
cd "$FRONTEND"
npm run dev &
FRONTEND_PID=$!
echo "Frontend started (PID $FRONTEND_PID) → http://localhost:5173"

echo ""
echo "Press Ctrl+C to stop both servers."

# Stop both on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
