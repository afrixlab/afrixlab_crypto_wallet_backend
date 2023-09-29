from celery import shared_task
from django.contrib.auth import get_user_model

from apps.utils.helpers import (
    EmailClient
)


@shared_task
def send_email_to_user(user_id: int, subject, message):
    UserModel = get_user_model()
    instance = UserModel.objects.get(id=user_id)
    email_messaging_helper = EmailClient(
        instance.email, subject, message, instance.short_name
    )
    email_messaging_helper.send_mail()