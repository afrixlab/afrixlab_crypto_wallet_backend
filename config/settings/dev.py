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