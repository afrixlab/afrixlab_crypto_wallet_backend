from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission


from apps.utils.helpers.commons import (
    DateTime
)
from apps.utils.enums import (
    UserAccountType
)

UserModel = get_user_model()


class IsGuestUser(BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    message: str

    def has_permission(self, request, view):
        self.message = "You are already logged in"
        return not request.user.is_authenticated



class EnforceUserBan(BasePermission):
    """
    Does not allow access to banned users
    """

    message: str

    def has_permission(self, request, view):
        self.message = "You have been banned for %s" % (
            DateTime.natural_time(request.user.suspend_duration_in_minutes)
        )
        return not bool(request.user.is_suspended and not request.user.is_super_admin)


class IsAccountType:
    class SuperAdminUser(BasePermission):
        """
        Allows access only to super admin users.
        """

        message: str

        def has_permission(self, request, view):
            self.message = "This endpoint is only for super admins"
            return (
                request.user.account_type
                == UserAccountType.SUPER_ADMINISTRATOR.value
            )

    class AdminUser(BasePermission):
        """
        Allows access only to admin users.
        """

        message: str

        def has_permission(self, request, view):
            self.message = "You are not an admin!"
            return request.user.account_type in [
                UserAccountType.ADMINISTRATOR.value,
                UserAccountType.SUPER_ADMINISTRATOR.value,
            ]
    class IsOwner(BasePermission):
        """
        def has_permission(self, request, view):
            print(view)
            return super().has_permission(request, view)
        """
        
        def has_object_permission(self, request, view, obj):
            #print(obj,obj.id,obj.owner)
            return request.user == obj.owner or request.user.is_staff 
            

    class NonAdminUser(BasePermission):
        """
        Allows access only to non-admin users.
        """

        message: str

        def has_permission(self, request, view):
            self.message = "You are not a base user!"
            return request.user.account_type == UserAccountType.USER.value


class IsVerified:
    class Email(BasePermission):
        """
        Allows access only to users with verified email.
        """

        message: str

        def has_permission(self, request, view):
            self.message = "Your email is not verified!"
            return (
                request.user.account_type == UserAccountType.ADMINISTRATOR.value
                or (request.user.email and request.user.is_email_verified)
            )


    class BaseUser(BasePermission):
        """
        Allows access only to users that are verified as a basic user.
        """

        message: str

        def has_permission(self, request, view):
            self.message = "You are not yet verified as normal user"
            return request.user.is_verified



class IsNotVerified:
    class BaseUser(BasePermission):
        """
        Allows access only to users that are not verified as a basic user.
        """

        message: str

        def has_permission(self, request, view):
            self.message = "You are verified as a base user!"
            return not request.user.is_verified





