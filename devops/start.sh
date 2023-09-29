#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py migrate
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload