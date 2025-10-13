#!/bin/sh

set -e

echo "FASTAPI_ENV: $FASTAPI_ENV"

HOST=${APP_HOST:-0.0.0.0}
PORT=${APP_PORT:-8080}
PROJECT_PATH=${PROJECT_PATH:-app}

if [ "$FASTAPI_ENV" = "production" ]; then
    echo "Starting the production server"
    exec gunicorn \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind ${HOST}:${PORT} \
        --config ${PROJECT_PATH}/core/gunicorn_conf.py \
        ${PROJECT_PATH}.main:app
else
    echo "Starting the development server"
    exec uvicorn \
        --reload \
        --host ${HOST} \
        --port ${PORT} \
        --log-level debug \
        --no-access-log \
        ${PROJECT_PATH}.main:app
fi