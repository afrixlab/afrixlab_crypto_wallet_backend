from django.contrib.auth import get_user_model
from rest_framework import serializers




class UserSerializer:
    class Update(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = [
                "username",
                "first_name",
                "last_name",
                "email",
                "username",
                "is_suspended",
                "is_verified",
                "account_type",
            ]

            ref_name = "User - Update"

    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            exclude = [
                "id",
                "password",
                "is_superuser",
                "is_staff",
                "groups",
                "user_permissions",
                "old_passwords",
            ]

            ref_name = "User - Retrieve"

