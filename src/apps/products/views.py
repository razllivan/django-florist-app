from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.products.filters import ProductFilter
from apps.products.models import Category, Image, Product, ProductImage, Size
from apps.products.serializers import (
    CategorySerializer,
    ImageSerializer,
    ProductImageSerializer,
    ProductSerializer,
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
    parser_classes = (MultiPartParser,)
    http_method_names = ["get", "post", "put", "delete"]


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
    serializer_class = ProductSerializer


class BaseProductRelatedViewSet(ModelViewSet):
    model = None

    def __init__(self, *args, **kwargs):
        if not self.model:
            raise AttributeError(
                "Subclasses must specify the 'model' attribute"
            )
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # Return a fake queryset for schema generation
            return self.model.objects.none()
        product_id = self.kwargs["product_id"]
        return self.model.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(product=product)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset and "product_id" in self.kwargs:
            product_id = self.kwargs.get("product_id")
            get_object_or_404(Product, pk=product_id)
        return super().list(request, *args, **kwargs)


class ProductImagesViewSet(BaseProductRelatedViewSet):
    model = ProductImage
    serializer_class = ProductImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "image_id"
