from rest_framework import serializers

from apps.products.models import Category, Size


class CategorySerializer(serializers.ModelSerializer):
    child_categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Category
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
