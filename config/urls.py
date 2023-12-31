from django.urls import (
    path,
    include,
    re_path
)
from django.contrib import admin
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Vaults Wallet API Documentation",
        default_version="v1",
        description="API Documentation for Vault Wallet backend",
        terms_of_service="",
        contact=openapi.Contact(email="@afrixlab.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/",admin.site.urls),
    path(f"api/v{settings.API_VERSION}/auth/",include("apps.user.urls")),
    path(f"api/v{settings.API_VERSION}/chain/",include("apps.chain.urls")),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]
