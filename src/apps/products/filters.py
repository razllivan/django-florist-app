import django_filters

from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):
    no_categories = django_filters.BooleanFilter(
        field_name="categories", lookup_expr="isnull"
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
