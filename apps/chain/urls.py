from django.conf import settings
from rest_framework import routers
from apps.chain.views import ChainViewSet

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()
    
app_name = "chain"
router.register("",ChainViewSet,basename="chains")
urlpatterns = router.urls