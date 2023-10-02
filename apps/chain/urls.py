from django.conf import settings
from rest_framework import routers
from apps.chain.views import ChainViewSet,CoinViewSet

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()
    
app_name = "chain"
router.register("",ChainViewSet,basename="chains")
router.register("coin",CoinViewSet,"coin")
urlpatterns = router.urls