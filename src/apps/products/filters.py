import django_filters
from django_filters import BaseInFilter, NumberFilter

from apps.products.models import Product


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ProductFilter(django_filters.FilterSet):
    uncategorized = django_filters.BooleanFilter(
        field_name="categories", lookup_expr="isnull", distinct=True
    )
    categories = NumberInFilter(
        field_name="categories", lookup_expr="in", distinct=True
    )

    class Meta:
        model = Product
        fields = [
            "uncategorized",
            "categories",
            "slug",
            "is_active",
            "is_archived",
        ]
