from rest_framework import (
    status,
    viewsets,
    response,
    decorators
)
from drf_yasg.utils import swagger_auto_schema
from apps.utils.mixins import (
    CustomRequestDataValidationMixin
)

from apps.utils import (
    permissions,
    exceptions
)
from apps.chain import (
    models,
    serializers
)
class ChainViewSet(
    CustomRequestDataValidationMixin,
    viewsets.ModelViewSet
):
    queryset = models.Chain.objects.all()
    serializer_class = serializers.ChainSerializer
    
    def get_required_fields(self):
        print(self.action)
        return []
    
    def get_permissions(self):
        if self.action in [
            "add_new_chain",
            "update_chain",
            "delete_chain"
        ]:
            return super().get_permissions() + [permissions.IsAccountType.AdminUser()]
        elif self.action == "list":
            return [permissions.IsGuestUser()]
        return super().get_permissions()
    
    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @decorators.action(detail=False,methods=["post"])
    def add_new_chain(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        raise exceptions.CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=[serializer.errors]
        )
    
    @decorators.action(
        detail=True,
        methods=['patch']
    )
    def update_chain(self, request, *args, pk=None):
        try:
            chain = self.get_object()
        except models.Chain.DoesNotExist:
            raise exceptions.CustomException(
                status.HTTP_404_NOT_FOUND,
                "Blockchain was not found"
            )
        serializer = self.get_serializer(chain, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @decorators.action(detail=True, methods=['delete'])
    def delete_chain(self, request, pk=None):
        try:
            coin = self.get_object()
        except models.Chain.DoesNotExist:
            raise exceptions.CustomException(
                status.HTTP_404_NOT_FOUND,
                "Chain was not found"
            )
        coin.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        
class CoinViewSet(
    CustomRequestDataValidationMixin,
    viewsets.ModelViewSet
):
    queryset = models.Coin.objects
    serializer_class = serializers.CoinSerializer
    
    def get_required_fields(self):
        return []
    
    def get_permissions(self):
        if self.action in [
            "add_new_coin",
            "delete_coin",
            "update_coin"
        ]:
            return super().get_permissions() + [permissions.IsAccountType.AdminUser()]
        elif self.action == "list":
            return [permissions.IsGuestUser()]
        return super().get_permissions()
    
    
    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @decorators.action(detail=False,methods=["post"])
    def add_new_coin(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        raise exceptions.CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=[serializer.errors]
        )
        
    @decorators.action(
        detail=True,
        methods=['patch']
    )
    def update_coin(self, request, *args, pk=None):
        try:
            coin = self.get_object()
        except models.Coin.DoesNotExist:
            raise exceptions.CustomException(
                status.HTTP_404_NOT_FOUND,
                "Coin was not found"
            )
        serializer = self.get_serializer(coin, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @decorators.action(detail=True, methods=['delete'])
    def delete_coin(self, request, pk=None):
        try:
            coin = self.get_object()
        except models.Chain.DoesNotExist:
            raise exceptions.CustomException(
                status.HTTP_404_NOT_FOUND,
                "Coin was not found"
            )
        coin.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        
        