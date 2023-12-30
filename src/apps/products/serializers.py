from rest_framework.fields import CharField
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
    size_description = CharField(write_only=True, required=False)

    def create(self, validated_data):
        fields_to_process = ["size_description"]

        image_data = {
            field: validated_data.pop(field)
            for field in fields_to_process
            if field in validated_data
        }

        image_data["img"] = validated_data.pop("new_image")

        image_instance = Image.objects.create(**image_data)
        validated_data["image"] = image_instance

        return super().create(validated_data)

    def update(self, instance, validated_data):
        fields_to_process = ["new_image", "size_description"]

        image_data = {
            field: validated_data.pop(field)
            for field in fields_to_process
            if field in validated_data
        }

        if image_data.get("new_image"):
            image_data["img"] = image_data.pop("new_image")
            image_instance = Image.objects.create(**image_data)
            instance.image = image_instance
        else:
            for field_name, field_data in image_data.items():
                setattr(instance.image, field_name, field_data)
        instance.save()
        return super().update(instance, validated_data)

    class Meta:
        model = ProductImage
        fields = [
            "new_image",
            "size_description",
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
