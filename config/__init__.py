from __future__ import absolute_import
import os
import sys
from pathlib import Path
import environ


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "apps"))
env = environ.Env()

env_path = os.path.join(BASE_DIR, "envs", ".env")
if os.path.exists(env_path):
    environ.Env.read_env(env_path, overwrite=True)
