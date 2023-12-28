from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
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


class ProductImagesViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # Return a fake queryset for schema generation
            return ProductImage.objects.none()
        product_id = self.kwargs["product_id"]
        return ProductImage.objects.filter(product_id=product_id)

    def retrieve(self, request, *args, **kwargs):
        image_id = kwargs.get("pk")
        product_id = self.kwargs.get("product_id")
        image = get_object_or_404(
            ProductImage, image_id=image_id, product_id=product_id
        )
        serializer = self.get_serializer(image)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        image_id = kwargs.get("pk")
        product_id = self.kwargs.get("product_id")
        image = get_object_or_404(
            ProductImage, image_id=image_id, product_id=product_id
        )
        serializer = self.get_serializer(
            image, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        get_object_or_404(Product, pk=product_id)
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        image_id = kwargs.get("pk")
        product_id = self.kwargs.get("product_id")
        image = get_object_or_404(
            ProductImage, image_id=image_id, product_id=product_id
        )
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
