from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.products.views import (
    CategoryViewSet,
    ImageViewSet,
    ProductViewSet,
    SizeViewSet,
)

app_name = "products"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"sizes", SizeViewSet)
router.register(r"images", ImageViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
