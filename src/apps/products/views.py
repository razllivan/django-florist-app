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
    ListProductMixin,
    PerformCreateProductMixin,
    ProductRelationsMixin,
)


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


class ProductImagesViewSet(
    ListProductMixin,
    PerformCreateProductMixin,
    ProductRelationsMixin,
    ModelViewSet,
):
    model = ProductImage
    serializer_class = ProductImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "image_id"


class ProductSizesViewSet(
    ListProductMixin, ProductRelationsMixin, ModelViewSet
):
    model = ProductSize
    serializer_class = ProductSizeSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "size_id"
    parser_classes = (JSONParser,)

class LinkProductSizeAPIView(PerformCreateProductMixin, CreateAPIView):
    model = ProductSize
    serializer_class = LinkProductSizeSerializer
