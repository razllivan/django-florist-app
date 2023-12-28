from rest_framework.serializers import (
    ImageField,
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
    image = ImageSerializer(read_only=True)
    new_image = ImageField(write_only=True)

    def create(self, validated_data):
        return self._create_or_update_image(validated_data)

    def update(self, instance, validated_data):
        return self._create_or_update_image(validated_data, instance)

    def _create_or_update_image(self, validated_data, instance=None):
        # sourcery skip: use-named-expression
        new_image = validated_data.pop("new_image", None)
        if new_image:
            image_instance = Image.objects.create(img=new_image)
            validated_data["image"] = image_instance
        if instance:
            instance.image = validated_data.get("image", instance.image)
            instance.save()
            return super().update(instance, validated_data)
        else:
            return super().create(validated_data)

    class Meta:
        model = ProductImage
        fields = [
            "new_image",
            "image",
            "is_preview",
        ]
        depth = 1


class ProductSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(
        many=True, source="productimage_set", read_only=True
    )

    categories_ids = PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Category.objects.all(),
        write_only=True,
    )
    sizes_ids = PrimaryKeyRelatedField(
        many=True, required=False, queryset=Size.objects.all(), write_only=True
    )
    images_ids = PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Image.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Product
        fields = "__all__"
