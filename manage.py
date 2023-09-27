#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent

env = environ.Env()

def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "apps"))
    execute_from_command_line(sys.argv)


env_path = os.path.join(BASE_DIR, "envs", ".env")


if os.path.exists(env_path):
    environ.Env.read_env(env_path)
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    env.str("DJANGO_SETTINGS_MODULE", "config.settings.local"),
)


if __name__ == "__main__":
    main()
