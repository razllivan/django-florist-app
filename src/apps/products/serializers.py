from rest_framework import serializers

from apps.products.models import Category, Image, Product, Size


class CategorySerializer(serializers.ModelSerializer):
    child_categories = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Category
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Category.objects.all()
    )
    sizes = SizeSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductReadSerializer(ProductWriteSerializer):
    categories = CategorySerializer(many=True)
