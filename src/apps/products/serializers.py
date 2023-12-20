from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.products.models import Category, Image, Product, Size


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


class ProductWriteSerializer(ModelSerializer):
    categories = PrimaryKeyRelatedField(
        many=True, required=False, queryset=Category.objects.all()
    )
    sizes = SizeSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductReadSerializer(ProductWriteSerializer):
    categories = CategorySerializer(many=True)
