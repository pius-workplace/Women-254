#!/usr/bin/env bash
set -euo pipefail
export $(grep -v '^#' .env | xargs -d '\n' -r)
export APP_HOST=${APP_HOST:-0.0.0.0}
uvicorn main:app --host $APP_HOST --port ${APP_PORT:-8000} --reload
