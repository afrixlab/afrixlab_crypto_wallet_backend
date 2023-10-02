from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_verified",
        ]

        ref_name = "Base User"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "old_passwords",
        ]
    class Update(serializers.ModelSerializer):
        username = serializers.CharField(
            allow_blank=False,
            allow_null=True,
            max_length=150,
        )
        
        class Meta:
            model = get_user_model()
            fields = [
                "first_name",
                "last_name",
                "email",
                "username",
                "is_supended",
                "suspend_duration_in_minutes",
            ]

            ref_name = "User - Update"

    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            exclude = [
                "password",
                "is_superuser",
                "is_staff",
                "groups",
                "user_permissions",
                "old_passwords",
            ]

            ref_name = "User - Retrieve"

