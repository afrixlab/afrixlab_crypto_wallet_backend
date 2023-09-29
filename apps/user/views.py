from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import (
    viewsets,
    decorators,
    status,
    response
)
from apps.utils.mixins import (
    CountListResponseMixin,
    CustomRequestDataValidationMixin
)
from apps.user import (
    serializers
)
from apps.utils  import (
    permissions,
    exceptions
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
        
        return []
    
    def get_permissions(self):
        if self.action in [
            "create_user_with_email_and_password",    
        ]:
            return [permissions.IsGuestUser()]
        
        return super().get_permissions()
    
    @decorators.action(
        detail=False,
        methods=['post'],
        url_name="create user with email and password",
        url_path="signup/create_user_with_email_and_password"
    )
        
    def create_user_with_email_and_password(self,request,*args, **kwargs):
        instance  = request.data
        if UserModel.objects.filter(email=instance['email']).exists():
            raise exceptions.CustomException(
                status_code=status.HTTP_409_CONFLICT,
                message="User with email exist"
            )
                
        user = UserModel.objects.create(**instance)
        user.set_password(instance['password'])
        user.is_password_set = True
        user.save()
        serializer = self.serializer_class.Retrieve(instance=user)
        response_data = {**serializer.data}
        return response.Response(
            status=status.HTTP_200_OK,
            data=response_data,
        )
