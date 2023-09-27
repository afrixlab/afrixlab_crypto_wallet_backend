"""
ASGI config for afrixlab crypto wallet project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
import django
from django.core.asgi import get_asgi_application
from . import env
django.setup()

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    env.str('DJANGO_SETTINGS_MODULE','config.settings.local')
)

application = get_asgi_application()
