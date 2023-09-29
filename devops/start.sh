#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py migrate
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload
gunicorn config.wsgi:application --workers 3 --worker-class gevent --worker-connections 2000 --bind 0.0.0.0:8000 --max-requests 50 --max-requests-jitter 20 --timeout 0 --log-level debug --access-logfile -
