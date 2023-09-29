from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers



class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "date_joined",
            "is_verified",
        ]

        ref_name = "Base User"


class UserSerializer:
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
                "google_auth_credentials",
            ]

            ref_name = "User - Retrieve"

