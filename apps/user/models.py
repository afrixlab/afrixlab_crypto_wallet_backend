import uuid
from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser
)
from django.utils.translation import gettext_lazy as _

from apps.utils.enums import (
    BaseModelMixin,
    UserAccountType
)



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError("The email field must not be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, account_type: str = UserAccountType.SUPER_ADMINISTRATOR.value, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if account_type != UserAccountType.SUPER_ADMINISTRATOR.value or account_type not in UserAccountType.values():
            raise ValueError("Invalid account type for a superuser")

        extra_fields.setdefault("account_type", account_type)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)

    def get_by_username(self, username: str):
        return self.get(username=username)



class User(AbstractUser, BaseModelMixin):
    
    id = models.UUIDField(
        _("User Id"),
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    
    first_name = models.CharField(
        _("First Name"), 
        null=True, 
        blank=True, 
        max_length=35
    )
    
    last_name = models.CharField(
        _("Last Name"), 
        null=True, 
        blank=True, 
        max_length=55
    )
    
    email = models.EmailField(
        _("Email"), 
        null=True, 
        blank=False, 
        max_length=225, 
        unique=True
    )
    
    username = models.CharField(
        _("Username"), 
        null=True, 
        blank=False, 
        max_length=80, 
        unique=True
    )
    
    account_type = models.CharField(
        _("Account Type"),
        choices=UserAccountType.choices(),
        default=UserAccountType.USER.value,
        null=False,
        blank=False,
        max_length=25,
    )
    
    wallet_phrase = models.CharField(
        _("User Wallet Phrase"),
        null=True,
        blank=False,
        max_length=255,
        unique=True,
    )
    
    oauth_username = models.CharField(
        _("Authentication Username"),
        null=True,
        blank=False,
        max_length=150,
        unique=True,
    )
    
    is_email_verified = models.BooleanField(
        _("Email Verified?"), 
        default=False, 
        blank=True, 
        null=False
    )
    
    can_get_notification = models.BooleanField(
        _("Can User get email notification?"),
        default=True,
        blank=False,
        null=False
    )
   
   