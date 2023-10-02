#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --max-interval 10
