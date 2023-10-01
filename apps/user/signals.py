from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

from apps.utils import (
    helpers,
    redis,
    message_templates 
)
UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        token = helpers.Token.create_random_hex_token(16)
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_email_verification_token_cache_reference(token),
            ttl=settings.EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS,
        )
        cache_instance.cache_value = {"owner": instance.id}
        message = message_templates.MessageTemplates.email_verification_email(token, settings.BASE_PAGE_URL)
        instance.send_mail("Email Verification", message)
