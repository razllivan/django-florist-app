from rest_framework.viewsets import ModelViewSet

from apps.products.models import Category
from apps.products.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
