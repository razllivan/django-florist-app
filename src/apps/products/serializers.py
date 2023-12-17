from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    child_categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Category
        fields = "__all__"
