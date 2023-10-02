from rest_framework import (
    status,
    viewsets,
    response,
    decorators
)

from apps.utils.mixins import (
    CountListResponseMixin,
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
    viewsets.ViewSet
):
    queryset = models.Chain.objects
    serializer_class = serializers.ChainSerializer
    
    def get_required_fields(self):
        if self.action == "add_new_chain":
            return [
                "id",
                "chain_name",
                "chain_symbol",
                "chain_type",
                "chain_logo",
            ]
        return []
    
    def get_permissions(self):
        if self.action in [
            "add_new_chain"
        ]:
            return super().get_permissions() + [permissions.IsAccountType.AdminUser()]
        return super().get_permissions()
    
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
        