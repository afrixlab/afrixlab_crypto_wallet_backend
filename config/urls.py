from django.urls import (
    path,
    include
)
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path("admin/",admin.site.urls),
    path(f"api/v{settings.API_VERSION}/auth/",include("apps.user.urls")),
]
