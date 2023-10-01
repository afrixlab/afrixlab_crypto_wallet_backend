import uuid, secrets

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser
)
from django.utils.translation import gettext_lazy as _

from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


from apps.user import tasks as celery_tasks
from apps.utils.enums import (
    BaseModelMixin,
    UserAccountType,
    create_token
)
from config.celery.queue import CeleryQueue


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
    #No default till our create wallet endpoint is done
    wallet_phrase = models.CharField(
        _("User Wallet Phrase"),
        null=True,
        blank=False,
        max_length=255,
        unique=True,
    )
    
    primary_picture = models.FileField(
        upload_to="vault/",
        null=True,
        blank=True,
    )
    old_passwords = models.BinaryField(
        null=True,
        blank=True, 
        editable=False, 
        verbose_name=_("Old Passwords")
    )
    is_password_set = models.BooleanField(
        _("Password has been set"), 
        null=False, 
        blank=False, 
        default=False
    )
    is_verified = models.BooleanField(
        _("User account has been verified"), null=False, blank=False, default=False
    )
    is_suspended = models.BooleanField(
        _("User account has been suspended"), null=False, blank=False, default=False
    )
    suspend_expiry_date = models.DateTimeField(
        _("User account suspend expiry date"), null=True, blank=True
    )
    suspend_duration_in_minutes = models.PositiveIntegerField(
        _("Suspend duration in minutes"), null=False, blank=False, default=0
    )
    otp = models.CharField(
        _("Otp"), default="0000", max_length=6, blank=True, null=True
    )
    
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        
    def set_google_auth_credentials(self, credentials: dict):
        self.google_auth_credentials = credentials
        self.save()
        
    @property
    def is_admin(self):
        return (
            self.account_type and self.account_type != UserAccountType.USER.value
        )

    @property
    def is_super_admin(self):
        return self.account_type == UserAccountType.SUPER_ADMINISTRATOR.value

    @property
    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    @property
    def short_name(self):
        return self.first_name or self.username or self.last_name or ""

    @property
    def short_name_with_username_as_priority(self):
        return self.username or self.first_name or self.last_name or ""

    @property
    def is_admin_type(self):
        return self.account_type in [
            UserAccountType.ADMINISTRATOR.value,
            UserAccountType.SUPER_ADMINISTRATOR.value,
        ]


    def verify_email(self):
        self.is_verified = True
        self.save()

    def retrieve_auth_token(self):
        data = {}
        refresh = RefreshToken.for_user(self)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

    def send_mail(self, subject, message, ignore_verification=True):
        assert self.email, f"User {self.id} does not have a valid email address"
        if not ignore_verification and not self.is_verified:
            return
        celery_tasks.send_email_to_user.apply_async(
            (self.id, subject, message),
            queue=CeleryQueue.Definitions.EMAIL_NOTIFICATION,
        )

        
    

    def notify_user(self, subject, message) -> bool:
        try:
            self.send_mail(subject, message)
            return True
        except Exception:
            return False
        
        
    def get_suitable_username_base(self):
        email = self.email
        first_name = self.first_name
        last_name = self.last_name
        return (
            (email and email.split("@")[0])
            or first_name
            or last_name
            or ("vault" + str(int(timezone.now().timestamp())).strip())
        ).replace(" ", "")

    @property
    def generate_username(self,email=None) -> str:
        if not email: 
            username_base = self.get_suitable_username_base()
        else:
            username_base = email
        username = username_base
        while True:
            if self.__class__.objects.filter(username=username).exists():
                username = username_base + str(secrets.randbelow(1000))
            else:
                break
        return username.lower()

    
    def __str__(self):
        return f"< {type(self).__name__}({self.id}) >"
    

class UserSession(BaseModelMixin):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh = models.CharField(max_length=255, unique=True, null=True, blank=True)
    access = models.CharField(max_length=255, unique=True, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        return f"{self.user} - {self.last_activity}"

class EmailVerificationToken(BaseModelMixin):
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="email_reset_tokens",
        verbose_name=_("Created By"),
    )
    token = models.CharField(
        _("Token"),
        null=False,
        blank=True,
        default=create_token,
        editable=False,
        max_length=100,
    )

    @property
    def is_expired(self):
        return timezone.now() > (
            self.date_added
            + timezone.timedelta(seconds=settings.PASSWORD_RESET_TOKEN_EXPIRATION_SECS)
        )


class PasswordResetToken(BaseModelMixin):
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="password_reset_tokens",
        verbose_name=_("Created By"),
    )
    token = models.CharField(
        _("Token"),
        null=False,
        blank=True,
        default=create_token,
        editable=False,
        max_length=100,
    )

    @property
    def is_expired(self):
        return timezone.now() > (
            self.date_added
            + timezone.timedelta(seconds=settings.PASSWORD_RESET_TOKEN_EXPIRATION_SECS)
        )
