import django_filters
from django_filters import BaseInFilter, NumberFilter

from apps.products.models import Product


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ProductFilter(django_filters.FilterSet):
    no_categories = django_filters.BooleanFilter(
        field_name="categories", lookup_expr="isnull", distinct=True
    )
    categories = NumberInFilter(
        field_name="categories", lookup_expr="in", distinct=True
    )

    class Meta:
        model = Product
        fields = [
            "no_categories",
            "categories",
            "slug",
            "is_active",
            "is_archived",
        ]
