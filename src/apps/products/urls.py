from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.products.views import (
    CategoryViewSet,
    ImageViewSet,
    ProductCategoriesViewSet,
    ProductImagesViewSet,
    ProductSizesViewSet,
    ProductViewSet,
    SizeViewSet,
)

app_name = "products"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"sizes", SizeViewSet)
router.register(r"images", ImageViewSet)
router.register(r"products", ProductViewSet)

product_images_router = DefaultRouter()
product_images_router.register(
    r"images", ProductImagesViewSet, basename="productimages"
)

product_sizes_router = DefaultRouter()
product_sizes_router.register(
    r"sizes", ProductSizesViewSet, basename="productsizes"
)

product_categories_router = DefaultRouter()
product_categories_router.register(
    r"categories", ProductCategoriesViewSet, basename="productcategories"
)

urlpatterns = [
    path("", include(router.urls)),
    path("products/<int:product_id>/", include(product_images_router.urls)),
    path("products/<int:product_id>/", include(product_sizes_router.urls)),
    path(
        "products/<int:product_id>/", include(product_categories_router.urls)
    ),
]
