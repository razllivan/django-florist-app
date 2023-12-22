from rest_framework.serializers import (
    ImageField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
)

from apps.products.models import Category, Image, Product, ProductImage, Size


class CategorySerializer(ModelSerializer):
    child_categories = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ProductImageSerializer(ModelSerializer):
    id = IntegerField(source="image.id")
    img = ImageField(source="image.img")

    class Meta:
        model = ProductImage
        fields = ["id", "img", "is_preview"]


class ProductWriteSerializer(ModelSerializer):
    categories = PrimaryKeyRelatedField(
        many=True, required=False, queryset=Category.objects.all()
    )
    sizes = PrimaryKeyRelatedField(
        many=True, required=False, queryset=Size.objects.all()
    )
    images = PrimaryKeyRelatedField(
        many=True, required=False, queryset=Image.objects.all()
    )

    class Meta:
        model = Product
        fields = "__all__"


class ProductReadSerializer(ProductWriteSerializer):
    categories = CategorySerializer(many=True)
    sizes = SizeSerializer(many=True)
    images = ProductImageSerializer(many=True, source="productimage_set")
