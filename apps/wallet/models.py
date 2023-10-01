from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.utils.enums import (
    BaseModelMixin,
)


UserModel = get_user_model()

class Wallet(BaseModelMixin):
    owner = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_wallet",
        verbose_name= _("Wallet Owner")
    )
    private_key = models.CharField(
        _("Wallet Private Key"),
        max_length=255,
        null=False,
        blank=False,
        default="***"
    )
    
