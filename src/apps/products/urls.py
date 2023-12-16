from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet

app_name = "products"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
