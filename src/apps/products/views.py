from rest_framework.viewsets import ModelViewSet

from apps.products.models import Category, Size
from apps.products.serializers import CategorySerializer, SizeSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ("is_active", "parent_category")


class SizeViewSet(ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
