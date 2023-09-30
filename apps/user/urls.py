from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views import AuthViewSet,AuthLoginView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "user"
router.register("", AuthViewSet, basename="auth")

urlpatterns = router.urls
urlpatterns += [
    path("login/", AuthLoginView.as_view(), name="auth_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


