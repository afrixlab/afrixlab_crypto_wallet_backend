from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()
from .models import UserSession


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("email","username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "primary_picture",     
                )
            },
        ),
        
        (
            _("Meta Information"),
            {
                "fields": (
                    "account_type",
                    "is_verified",
                )
            },
        ),
        
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "id",
        "email",
        "account_type",
        "is_verified",
        "is_superuser",
    ]
    search_fields = ["first_name", "last_name"]


admin.site.register(UserSession)

