"""
Django settings for afrixlab crypto wallet project.
"""
import os
from pathlib import Path
from config import env
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY",default="***")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG_MODE",default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOST",default=[
    "*"
])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
if env.bool("USE_DJANGO_DEFAULT_DB",True):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env.str("DJANGO_POSTGRESQL_ENGINE", "***"),
            "NAME": env.str("DJANGO_POSTGRESQL_NAME", "***"),
            "USER": env.str("DJANGO_POSTGRESQL_USER", "***"),
            "PASSWORD": env.str("DJANGO_POSTGRESQL_PASSWORD", "***"),
            "HOST": env.str("DJANGO_POSTGRESQL_HOST","***"),
            "PORT": env.int("DJANGO_POSTGRESQL_PORT", 5432),
        },    
    }



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
