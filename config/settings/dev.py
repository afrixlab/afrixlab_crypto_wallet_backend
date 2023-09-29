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

#____RESET PASSWORD TOKEN EXPIRATION TIME_____
PASSWORD_RESET_TOKEN_EXPIRATION_SECS = env.int(
    "PASSWORD_RESET_TOKEN_EXPIRATION_SECS", default=(3600 * 6)
)