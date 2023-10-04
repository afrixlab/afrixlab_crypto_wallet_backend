"""
WSGI config for afrixlab crypto wallet project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

from . import env
import os
import django
from django.core.wsgi import get_wsgi_application
django.setup()

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 
    env.str('DJANGO_SETTINGS_MODULE','config.settings.local'),
)
application = get_wsgi_application()
