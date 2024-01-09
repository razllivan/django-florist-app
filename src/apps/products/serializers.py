from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.products.models import (
    Category,
    Image,
    Product,
    ProductImage,
    ProductSize,
    Size,
)


class CategorySerializer(ModelSerializer):
    child_categories = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ProductSizeSerializer(ModelSerializer):
    size = SizeSerializer(read_only=True)

    class Meta:
        model = ProductSize
        fields = [
            "size",
            "price",
            "is_active",
        ]


class LinkProductSizeSerializer(ModelSerializer):
    size = PrimaryKeyRelatedField(queryset=Size.objects.all())

    class Meta:
        model = ProductSize
        fields = [
            "size",
            "price",
            "is_active",
        ]


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ProductImageSerializer(ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = ProductImage
        fields = [
            "image",
            "is_preview",
        ]


class LinkProductImageSerializer(ModelSerializer):
    image = PrimaryKeyRelatedField(queryset=Image.objects.all())

    class Meta:
        model = ProductImage
        fields = [
            "image",
            "is_preview",
        ]


class ProductSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    sizes = ProductSizeSerializer(
        many=True, read_only=True, source="productsize_set"
    )
    images = ProductImageSerializer(
        many=True, source="productimage_set", read_only=True
    )

    categories_ids = PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Category.objects.all(),
        write_only=True,
        source="categories",
    )
    images_ids = PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Image.objects.all(),
        write_only=True,
        source="images",
    )

    class Meta:
        model = Product
        fields = "__all__"
