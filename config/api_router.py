from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from gatekeeper.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "users_api"
urlpatterns = router.urls
