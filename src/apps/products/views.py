from drf_spectacular.utils import extend_schema_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.products.filters import ProductFilter
from apps.products.mixins import (
    CreateMixin,
    ListProductMixin,
    PerformCreateProductMixin,
    ProductRelationsMixin,
)
from apps.products.models import (
    Category,
    Image,
    Product,
    ProductImage,
    ProductSize,
    Size,
)
from apps.products.schema import ProductImagesSchema, ProductSizesSchema
from apps.products.serializers import (
    CategorySerializer,
    ImageSerializer,
    LinkProductSizeSerializer,
    ProductImageSerializer,
    ProductSerializer,
    ProductSizeSerializer,
    SizeSerializer,
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


@extend_schema_view(
    list=ProductImagesSchema().list(),
    create=ProductImagesSchema().create(),
    retrieve=ProductImagesSchema().retrieve(),
    partial_update=ProductImagesSchema().partial_update(),
    destroy=ProductImagesSchema().destroy(),
)
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


@extend_schema_view(
    list=ProductSizesSchema().list(),
    create=ProductSizesSchema().create(),
    retrieve=ProductSizesSchema().retrieve(),
    partial_update=ProductSizesSchema().partial_update(),
    destroy=ProductSizesSchema().destroy(),
)
class ProductSizesViewSet(
    ListProductMixin,
    CreateMixin,
    PerformCreateProductMixin,
    ProductRelationsMixin,
    ModelViewSet,
):
    model = ProductSize
    serializer_class = ProductSizeSerializer
    serializer_create_class = LinkProductSizeSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "size_id"
    parser_classes = (JSONParser,)
