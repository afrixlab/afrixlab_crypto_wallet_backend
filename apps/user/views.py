import re
import orjson

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.http import QueryDict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
    CustomRequestDataValidationMixin,
    CountListResponseMixin,
    viewsets.ViewSet
):
    queryset = UserModel.objects
    serializer_class = serializers.UserSerializer
    http_method_names = ["post","get"]

    def get_queryset(self):
        return self.queryset.all()


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
        elif self.action in ["logout","finalize_verify_email"]:
            return ['token']
        
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
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email","password"],
            properties= {
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "account_type": openapi.Schema(type=openapi.TYPE_STRING,enum=enums.UserAccountType.values()),
                "primary_picture": openapi.Schema(type=openapi.TYPE_FILE)
            }
        ),
        responses={
            200: serializer_class.Retrieve(),
            409: "Conflict: User exist",
            400: "Bad Request. Invalid input data.",
        }
    )

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
        serializer = serializers.BaseUserSerializer(instance=user)
        response_data = {**serializer.data}
        return response.Response(
            status=status.HTTP_200_OK,
            data=response_data,
        )
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["token"],
            properties= {
                'token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            204: "No Content",
            404: "Token Error. Refresh token error",
        }
    )
    @decorators.action(
        detail=False, 
        methods=["post"],
    )
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
    
    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties= {
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Account Suspended",
            400: "Account already reported",
            404: "User not found",
            406: "Not Accpetable: it's an ADMINISTRATOR account"
        }
    )
    @decorators.action(
        detail=False,
        methods=['post'],
        url_name="suspend_user",
    )
    
    def suspend_user(self,request,*args, **kwargs):
        """
        The above function suspends a user account based on the provided email and returns a response
        with the status and a message.
        
        :param request: The `request` parameter represents the HTTP request object that contains
        information about the incoming request, such as headers, body, and query parameters
        :return: an HTTP response with a status code of 200 (OK) and a JSON object containing a
        "message" key with the value "Account Suspended".
        """
        email_username =  request.data.get("email")
        user = UserModel.objects.get(email=email_username)
        
        if not user:
            raise exceptions.CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User data does not exist"
            )
        if user.is_suspended:
            raise exceptions.CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
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
        
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties= {
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Account Unbanned",
            400: "Account not banned",
            403: "User not found",
        }
    )
    @decorators.action(
        detail=False,
        methods=['post'],
        url_name="unban user",
    )
    
    def unban_user(self,request,*args, **kwargs):
        """
        The `unban_user` function takes an email as input, retrieves the corresponding user from the
        database, checks if the user is currently banned, and if so, updates the `is_suspended` field to
        False to unban the user.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by
        the client. It contains information such as the request method, headers, body, and query
        parameters. In this code snippet, the `request` object is used to retrieve the email of the user
        to be unbanned
        :return: a response with a status code of 200 (OK) and a JSON object containing a message
        indicating that the account has been unbanned.
        """
        
        email_username =  request.data.get("email")
        user = UserModel.objects.get(email=email_username)
        
        if not user:
            raise exceptions.CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User data does not exist"
            )
        if not user.is_suspended:
            raise exceptions.CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="User not banned"
            )

        user.is_suspended = True
        user.save()
        
        return response.Response(
            status=status.HTTP_200_OK,
            data={"message": "Account Unbanned"},
        )
        
        
    @swagger_auto_schema(
        methods=["get", "patch"],
        query_serializer=serializer_class.Update,
        responses={
            200: serializer_class.Retrieve(),
            400: "Bad Request. Invalid input data.",
        }
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
            serializer = self.serializer_class.Update(
                instance=request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.serializer_class.Retrieve(instance=request.user)
            return response.Response(status=status.HTTP_200_OK, data=serializer.data)
        

    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["old_password","new_password"],
            properties= {
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: "Password changed successfully",
            400: "The new password must be different from the old passwords",
            403: "The old password you provided is incorrect"
        }
    )
    @decorators.action(detail=False, methods=["post"])
    def change_password(self, request, *args, **kwargs):
        """
        The `change_password` function allows a user to change their password by providing the old
        password and a new password, with validation checks for password correctness and uniqueness.
        
        :param request: The `request` parameter represents the HTTP request object that contains
        information about the incoming request, such as headers, body, and query parameters
        :return: a response with a status code of 200 (OK) and a JSON object containing a "message" key
        with the value "Password changed successfully".
        """
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        instance = request.user
        if not check_password(old_password, instance.password):
            raise exceptions.CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="The old password you provided is incorrect",
                errors=["incorrect old password"],
            )

        if check_password(new_password, instance.password):
            raise exceptions.CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
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



    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["page_base_url"],
            properties= {
                'page_base_url': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "A verification mail has been successfully sent to [ request sender email ]",
            403: "The email address is already verified for the account"
        }
    )
    @decorators.action(
        detail=False, 
        methods=["post"],
        url_name="Request Email Verification",
        url_path="request_email_verification"
    )
    def initialize_verify_email(self, request, *args, **kwargs):
        """
        The `initialize_verify_email` function sends a verification email to the user's email address if
        it is not already verified.
        
        :param request: The `request` parameter is an object that represents the HTTP request made to
        the API endpoint. It contains information about the request, such as the request method,
        headers, body, and user making the request
        :return: The function `initialize_verify_email` returns an HTTP response with a status code of
        200 (OK) and a JSON object containing a message indicating that a verification mail has been
        successfully sent to the email address associated with the user instance.
        """
        page_base_url = request.data.get("page_base_url")
        instance: models.User = request.user
        if instance.is_verified:
            raise exceptions.CustomException(
                status_code= status.HTTP_403_FORBIDDEN,
                message="The email address is already verified for the account",
                errors=["verified email"],
            )

        token = helpers.Token.create_random_hex_token(16)
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_email_verification_token_cache_reference(token),
            ttl=settings.EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS,
        )
        cache_instance.cache_value = {"owner": instance.id}
        message = MessageTemplates.MessageTemplates.email_verification_email(token, page_base_url)
        instance.send_mail("Email Verification", message)
        return response.Response(
            status=status.HTTP_200_OK,
            data={
                "message": f"A verification mail has been successfully sent to {instance.email}"
            },
        )



    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["token"],
            properties= {
                'token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Email verified successfully",
            403: "You specified an invalid token"
        }
    )
    @decorators.action(
        detail=False, 
        methods=["post"],
        url_name="Verify token for email",
        url_path="verify_email"
    )
    def finalize_verify_email(self, request, *args, **kwargs):
        """
        The `finalize_verify_email` function verifies an email using a token and sends a success message
        if the verification is successful.
        
        :param request: The `request` parameter represents the HTTP request object that contains
        information about the incoming request, such as headers, body, and query parameters
        :return: The function `finalize_verify_email` returns an HTTP response with a status code of 200
        (OK) and a JSON object containing a message indicating that the email has been verified
        successfully.
        """
        token = request.data.get("token")
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_email_verification_token_cache_reference(token),
            ttl=settings.EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS,
        )
        if not cache_instance.cache_value:
            raise exceptions.CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="You specified an invalid token",
                errors=["expired token"],
            )
        instance: UserModel = UserModel.objects.get(
            id=cache_instance.cache_value.get("owner")
        )
        instance.verify_email()
        cache_instance.cache_value = None
        message = MessageTemplates.MessageTemplates.email_verification_success()
        instance.send_mail("Email Verification Success", message)
        return response.Response(
            status=status.HTTP_200_OK,
            data={"message": f"Email verified successfully"},
        )
        
        
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email","page_base_url"],
            properties= {
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'page_base_url': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Password reset email has been successfully sent to [ request sender email ]"
        }
    )  
    @decorators.action(
        detail=False, 
        methods=["post"],
        url_path="reset-account"
    )
    def initiate_reset_password_email(self, request, *args, **kwargs):
        """
        This `initiate_reset_password_email` function sends a password reset email to the specified email
        address.
        
        :param request: The `request` parameter is an object that represents the HTTP request made to
        the API endpoint. It contains information such as the request method, headers, body, and query
        parameters
        :return: The function `initiate_reset_password_email` is returning an HTTP response with a
        status code of 200 (OK) and a JSON object as the response data. The response data includes a
        message indicating that the password reset email has been successfully sent to the specified
        email address.
        """,
        email = request.data.get("email").lower()
        instance = helpers.commons.Utils.get_object_or_raise_error(UserModel.objects, email=email)
        token = helpers.Token.create_random_hex_token(16)
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_password_reset_token_cache_reference(token),
            ttl=settings.PASSWORD_RESET_TOKEN_EXPIRATION_SECS,
        )
        cache_instance.cache_value = {"owner": instance.id}
        message = MessageTemplates.MessageTemplates.password_reset_email(
            token, request.data.get("page_base_url")
        )
        instance.send_mail(
            subject="Password Reset",
            message=message,
        )
        return response.Response(
            status=status.HTTP_200_OK,
            data={
                "message": f"Password reset email has been successfully sent to {email}"
            },
        )



    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["token","password"],
            properties= {
                'token': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Password changed successfully",
            403: "You specified an invalid token"
        }
    )  
    @decorators.action(
        detail=False, 
        methods=["post"],
        url_path="reset-password"
    )
    def finalize_reset_password_email(self, request, *args, **kwargs):
        """
        The above function is an API endpoint that allows users to finalize the reset password process
        by providing a token and a new password.
        
        :param request: The `request` parameter is the HTTP request object that contains information
        about the incoming request, such as headers, body, and query parameters. It is used to access
        the data sent in the request body using `request.data.get("token")` and
        `request.data.get("password")`
        :return: The function `finalize_reset_password_email` returns an HTTP response with a status
        code of 200 (OK) and a JSON object containing a message indicating that the password has been
        changed successfully.
        """
        token = request.data.get("token")
        password = request.data.get("password")
        cache_instance = redis.RedisTools(
            helpers.UserAuthHelpers.get_password_reset_token_cache_reference(token),
            ttl=settings.PASSWORD_RESET_TOKEN_EXPIRATION_SECS,
        )
        if not cache_instance.cache_value:
            raise exceptions.CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
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
    def check_login_status(view_func):
        def wrapper_func(self, request, *args, **kwargs):
            
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
            return view_func(self, request, *args, **kwargs)
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

        
    
        