from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views import AuthViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "user"
router.register("", AuthViewSet, basename="auth")

urlpatterns = router.urls
urlpatterns += [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

