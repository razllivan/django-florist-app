from rest_framework.viewsets import ModelViewSet

from apps.products.filters import ProductFilter
from apps.products.models import Category, Image, Product, Size
from apps.products.serializers import (
    CategorySerializer,
    ImageSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
    SizeSerializer,
)


class CategoryViewSet(ModelViewSet):
    """
    Fields:

        is_active (bool): Used to hide categories from the catalog.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ("is_active", "parent_category", "slug")


class SizeViewSet(ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ProductViewSet(ModelViewSet):
    """
    Fields:

        is_active (bool): Used to hide products from the catalog.

        is_archived (bool): In the future, products will be marked as
        archived instead of being deleted when referenced by an
        order. Archiving ensures that historical data integrity is maintained
        while the product.
    """

    queryset = Product.objects.all()
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ProductReadSerializer
        return ProductWriteSerializer
