from django.contrib.auth import get_user_model
from rest_framework import serializers



class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

        ref_name = "Base User"


class UserSerializer(BaseUserSerializer):
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

