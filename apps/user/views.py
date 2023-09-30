import re
import orjson
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.http import QueryDict

from rest_framework import (
    viewsets,
    decorators,
    status,
    response
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError


from apps.utils.mixins import (
    CountListResponseMixin,
    CustomRequestDataValidationMixin
)
from apps.user import (
    serializers,
    models
)
from apps.user.models import UserSession
from apps.utils  import (
    permissions,
    exceptions,
    enums,
    helpers,
    redis,
    message_templates as MessageTemplates
)

UserModel = get_user_model()


class AuthViewSet(
    CountListResponseMixin,
    CustomRequestDataValidationMixin,
    viewsets.ViewSet
):
    queryset = UserModel.objects
    serializer_class = serializers.UserSerializer

    def get_required_fields(self):
        if self.action == "create_user_with_email_and_password":
            return ["email","password"]
        elif self.action == "initialize_verify_email":
            return ["page_base_url"]
        elif self.action == "change_password":
            return ["old_password", "new_password"]
        elif self.action == "initiate_reset_password_email":
            return ["email"]
        elif self.action == "finalize_reset_password_email":
            return ["token", "password"]
        
        return []
    
    def get_permissions(self):
        if self.action in [
            "create_user_with_email_and_password",  
            "initiate_reset_password_email",
            "finalize_reset_password_email",
        ]:
            return [permissions.IsGuestUser()]
        elif self.action in [
            "suspend_user_account"
        ]:
            return super().get_permissions() + [permissions.IsAccountType.AdminUser()]
        
        return super().get_permissions()
    
    def password_validator(func):
        def create_user_with_email_and_password(self,request, *args, **kwargs):
            if "password" in request.data:
                password = request.data['password']
                if len(password) < 8:
                    raise exceptions.CustomException(message="Password must be at least 8 characters long")
                if not re.search(r'[A-Z]', password):
                    raise exceptions.CustomException(message="Password must contain at least one uppercase letter")
                if not re.search(r'[a-z]', password):
                    raise exceptions.CustomException(message="Password must contain at least one lowercase letter")
                if not re.search(r'[0-9]', password):
                    raise exceptions.CustomException(message="Password must contain at least one digit")
                if not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\-]', password):
                    raise exceptions.CustomException(message="Password must contain at least one special character")
            return func( self,request, *args, **kwargs)
        return create_user_with_email_and_password
    
    
    @decorators.action(
        detail=False,
        methods=['post'],
        url_name="create user with email and password",
        url_path="register"
    )
    @password_validator
    def create_user_with_email_and_password(self,request,*args, **kwargs):
        instance  = request.data
        if UserModel.objects.filter(email=instance['email']).exists():
            raise exceptions.CustomException(
                status_code=status.HTTP_409_CONFLICT,
                message="User exist"
            )
                
        user = UserModel.objects.create(**instance)
        user.set_password(instance['password'])
        user.is_password_set = True
        user.username = user.generate_username
        user.save()
        serializer = self.serializer_class.Retrieve(instance=user)
        response_data = {**serializer.data}
        return response.Response(
            status=status.HTTP_200_OK,
            data=response_data,
        )
    
    @decorators.action(detail=False, methods=["post"])
    def logout(self, request, *args, **kwargs):
        try:
            UserSession.objects.get(refresh=request.data.get("token")).delete()
            refresh_token = request.data.get("token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError as err:
            raise exceptions.CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(err),
                errors=["refresh token error"],
            )
        except UserSession.DoesNotExist as err:
            raise exceptions.CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(err),
                errors=["refresh token error"],
            )
            
    @decorators.action(
        detail=False,
        methods=['post'],
        url_name="suspend_default_user",
        url_path="user/suspend"
    )
    def suspend_user_account(self,request,*args, **kwargs):
        
        email_username =  request.data.get("email")
        user = UserModel.objects.get(email=email_username)
        
        if not user:
            raise exceptions.CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User data does not exist"
            )
        if user.is_suspended:
            raise exceptions.CustomException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                message="User already suspended"
            )
        
        if user.account_type != enums.UserAccountType.USER.value:
                raise exceptions.CustomException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    message="ADMINISTRATOR ACCOUNT"
                )
        
        user.is_suspended = True
        user.save()
        
        return response.Response(
            status=status.HTTP_200_OK,
            data={"message": "Account Suspended"},
        )
        
    @decorators.action(
        detail=False,
        methods=["get", "patch"],
        name="me",
        url_path="me",
    )
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            serializer = self.serializer_class.Retrieve(instance=request.user)
            return response.Response(status=status.HTTP_200_OK, data=serializer.data)
        elif request.method == "PATCH":
            unique_fields = ["email", "username","primary_picture"]
            base_queryset = self.queryset.exclude(id=request.user.id)
            for field in unique_fields:
                if request.data.get(field):
                    value = request.data.get(field)
                    if field == "username":
                        queryset = base_queryset.filter(username=value)
                    elif field == "email":
                        queryset = base_queryset.filter(email=value)
                    else:
                        queryset = base_queryset.filter(primary_picture=value)
                    if queryset.exists():
                        raise exceptions.CustomException(
                            errors=[f"{field} in use"],
                            message=f"The specified {field.replace('_', ' ')} is already in use by another user",
                        )

            serializer = self.serializer_class.Update(
                instance=request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.serializer_class.Retrieve(instance=request.user)
            return response.Response(status=status.HTTP_200_OK, data=serializer.data)
        
    @decorators.action(detail=False, methods=["post"])
    def change_password(self, request, *args, **kwargs):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        instance = request.user
        if not check_password(old_password, instance.password):
            raise exceptions.CustomException(
                message="The old password you provided is incorrect",
                errors=["incorrect old password"],
            )

        if check_password(new_password, instance.password):
            raise exceptions.CustomException(
                message="The new password must be different from the old passwords",
                errors=["same password"],
            )

        old_passwords = orjson.loads(instance.old_passwords or orjson.dumps([]))
        if new_password in old_passwords:
            raise exceptions.CustomException(
                errors=["password already used before"],
                message="The new password has been used before on this account",
            )

        instance.set_password(new_password)
        old_passwords.append(old_password)
        instance.old_passwords = orjson.dumps(old_passwords)
        instance.save()
        return response.Response(
            status=status.HTTP_200_OK,
            data={"message": "Password changed successfully"},
        )

    @decorators.action(detail=False, methods=["post"])
    def initialize_verify_email(self, request, *args, **kwargs):
        page_base_url = request.data.get("page_base_url")
        instance: models.User = request.user
        if instance.is_email_verified:
            raise exceptions.CustomException(
                message="The email address is already verified for the account",
                errors=["verified email"],
            )

        token = helpers.Token.create_random_hex_token(16)
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_email_verification_token_cache_reference(token),
            ttl=settings.EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS,
        )
        cache_instance.cache_value = {"owner": instance.id}
        message = MessageTemplates.email_verification_email(token, page_base_url)
        instance.send_mail("Email Verification", message)
        return response.Response(
            status=status.HTTP_200_OK,
            data={
                "message": f"An verification mail has been successfully sent to {instance.email}"
            },
        )

    @decorators.action(detail=False, methods=["post"])
    def finalize_verify_email(self, request, *args, **kwargs):
        token = request.data.get("token")
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_email_verification_token_cache_reference(token),
            ttl=settings.EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS,
        )
        if not cache_instance.cache_value:
            raise exceptions.CustomException(
                message="You specified an invalid token",
                errors=["expired token"],
            )
        instance: UserModel = UserModel.objects.get(
            id=cache_instance.cache_value.get("owner")
        )
        instance.verify_email()
        print(instance.is_email_verified)
        cache_instance.cache_value = None
        message = MessageTemplates.email_verification_success()
        instance.send_mail("Email Verification Success", message)
        return response.Response(
            status=status.HTTP_200_OK,
            data={"message": f"Email verified successfully"},
        )
        
    @decorators.action(
        detail=False, 
        methods=["post"],
        url_path="reset-account/"
    )
    def initiate_reset_password_email(self, request, *args, **kwargs):
        email = request.data.get("email").lower()
        instance = helpers.commons.Utils.get_object_or_raise_error(UserModel.objects, email=email)
        token = helpers.Token.create_random_hex_token(16)
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_password_reset_token_cache_reference(token),
            ttl=settings.PASSWORD_RESET_TOKEN_EXPIRATION_SECS,
        )
        cache_instance.cache_value = {"owner": instance.id}
        message = MessageTemplates.password_reset_email(
            token, request.data.get("page_base_url")
        )
        instance.send_mail(
            subject="Password Reset",
            message=message,
        )
        return response.Response(
            status=status.HTTP_200_OK,
            data={
                "message": f"An password reset email has been successfully sent to {email}"
            },
        )

    @decorators.action(
        detail=False, 
        methods=["post"],
        url_path="reset-password"
    )
    def finalize_reset_password_email(self, request, *args, **kwargs):
        token = request.data.get("token")
        password = request.data.get("password")
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_password_reset_token_cache_reference(token),
            ttl=settings.PASSWORD_RESET_TOKEN_EXPIRATION_SECS,
        )
        if not cache_instance.cache_value:
            raise exceptions.CustomException(
                message="You specified an invalid token",
                errors=["expired token"],
            )
        instance: UserModel = UserModel.objects.get(
            id=cache_instance.cache_value.get("owner")
        )
        instance.set_password(password)
        instance.save()
        cache_instance.cache_value = None
        return response.Response(
            status=status.HTTP_200_OK,
            data={"message": f"Password changed successfully"},
        )


class AuthLoginView(TokenObtainPairView):
    @staticmethod
    def check_login_status(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            if "email" not in request.data:
                raise exceptions.CustomException(
                    message="Email is required",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            session = UserSession.objects.filter(
                user__email=request.data["email"]
            ).first()

            if session and session.is_active:     
                try:
                    token = RefreshToken(session.refresh)
                    token.blacklist()
                except Exception as e:
                    raise exceptions.CustomException(message="unable to blacklist token")
                session.is_active = False
                session.save()
            return view_func(request, *args, **kwargs)
        return wrapper_func

    @check_login_status
    def post(self, request, *args, **kwargs):
        if not request.data.get("email"):
            raise exceptions.CustomException(
                message="Email is required",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data[UserModel.USERNAME_FIELD] = request.data["email"]
        response = super().post(request, *args, **kwargs)

        user = UserModel.objects.get(email=request.data["email"])
        session = UserSession.objects.filter(user=user).first()
        if session:
            session.is_active = True
            session.refresh = response.data["refresh"]
            session.access = response.data["access"]
            session.ip_address = request.META.get("REMOTE_ADDR")
            session.user_agent = request.META.get("HTTP_USER_AGENT")
            session.save()
        
        else:
            UserSession.objects.create(
                user=user,
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
                is_active=True,
                refresh=response.data["refresh"],
                access=response.data["access"],
            )
        return response

        
    
        