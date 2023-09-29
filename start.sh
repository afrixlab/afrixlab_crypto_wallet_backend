#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py migrate
gunicorn config.asgi:application --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 0 --log-level debug --access-logfile -
