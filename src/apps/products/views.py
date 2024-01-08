from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.filters import ProductFilter
from apps.products.mixins import (
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
    PerformCreateProductMixin,
    ProductRelationsMixin,
    ModelViewSet,
):
    model = ProductSize
    serializer_class = ProductSizeSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "size_id"
    parser_classes = (JSONParser,)

    def get_serializer_class(self):
        if self.action == "create":
            return LinkProductSizeSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = LinkProductSizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
