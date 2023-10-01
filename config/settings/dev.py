from .base import *

EMAIL_BACKEND = env.str("EMAIL_BACKEND",default="***")
EMAIL_USE_SSL= env.bool("EMAIL_USE_SSL",True)
EMAIL_USE_TSL= env.bool("EMAIL_USE_TSL",False)
EMAIL_HOST = env.str("EMAIL_HOST", default="***")
EMAIL_PORT = env.int("EMAIL_PORT",465)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="***")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="***")
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER

#___________ API AND VERSIONING ____________
API_VERSION = env.str("API_VERSION",default="1")

#____ RESET PASSWORD TOKEN EXPIRATION TIME _____
PASSWORD_RESET_TOKEN_EXPIRATION_SECS = env.int(
    "PASSWORD_RESET_TOKEN_EXPIRATION_SECS", default=(3600 * 6)
)

# ____________ EMAIL VERIFICATION ______________
EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS = env.int(
    "EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS", default=(3600 * 6)
)
# ____________________CLOUDINARY__________________________________

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env.str("CLOUDINARY_CLOUD_NAME",default="****"),
    "API_KEY": env.str("CLOUDINARY_API_KEY",default="****"),
    "API_SECRET": env.str("CLOUDINARY_API_SECRET",default="****")
}
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


#______________  SITE ___________
SITE_NAME = "Afrix Labs Vaults App"
BASE_PAGE_URL = env.str("BASE_PAGE_URL","http://127.0.0.1")

# _______________________Swagger _________________________
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
}

#______________________REDIS____________________________
REDIS_HOST = env.str("REDIS_HOST", default="localhost")
REDIS_PORT = env.int("REDIS_PORT", default=6379)

# ______________________ Cache _______________________________
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}"

    }
}
CACHE_TTL = env.int("VIEW_CACHE_TTL_SECS", 60 * 15)



# ___________________________________Celery_________________________________________
CELERY_BROKER = env.str("CELERY_BROKER", default="***********")
CELERY_BROKER_URL = CELERY_BROKER
CELERY_RESULT_BACKEND = env.str("CELERY_BACKEND", default="*************")
CELERY_TIMEZONE = env.str("CELERY_TIMEZONE", default="UTC")
CELERY_ACKS_LATE = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERYD_PREFETCH_MULTIPLIER = 1


#______________________ JAZZMIN __________________________________

JAZZMIN_SETTINGS = {
    "site_title": "Vault's Admin",
    "site_header": "Vault Crypto Wallet",
    "site_brand": "Vault's",
    "welcome_sign": "Welcome to Vault's wallet",
    "copyright": "Afrix Lab Ltd",
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,


    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": False,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    #"changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": True,
}