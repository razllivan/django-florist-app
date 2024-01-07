from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.products.filters import ProductFilter
from apps.products.models import (
    Category,
    Image,
    Product,
    ProductImage,
    ProductSize,
    Size,
)
from apps.products.serializers import (
    CategorySerializer,
    ImageSerializer,
    ProductImageSerializer,
    ProductSerializer,
    ProductSizeSerializer,
    SizeSerializer,
    LinkProductSizeSerializer,
)
from apps.products.mixins import (
    PerformCreateProductMixin,


class CategoryViewSet(ModelViewSet):
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


class ProductSizesViewSet(BaseProductRelatedViewSet):
    model = ProductSize
    serializer_class = ProductSizeSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "size_id"
    parser_classes = (JSONParser,)

class LinkProductSizeAPIView(PerformCreateProductMixin, CreateAPIView):
    model = ProductSize
    serializer_class = LinkProductSizeSerializer
