from __future__ import absolute_import, unicode_literals

import os
from pathlib import Path

import environ
from celery import Celery
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()

env_path = os.path.join(ROOT_DIR, "venv", ".env")
if os.path.exists(env_path):
    environ.Env.read_env(env_path)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", env.str("DJANGO_SETTINGS_MODULE", "config.settings.local")
)

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
