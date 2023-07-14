#! /usr/bin/env bash

# Run migrations
echo "Running Alembic migrations..."
sleep 10
alembic upgrade head

echo "Running Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
#gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000