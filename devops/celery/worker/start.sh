#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


celery -A config worker -Q email-notification,beats -l INFO
