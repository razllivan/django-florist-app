import pytest

from apps.products.filters import ProductFilter
from apps.products.models import Product
from apps.products.tests.factories import ProductFactory


@pytest.mark.django_db
def test_no_categories_filter_excludes_categorized_products(category):
    """
    Test 'no_categories' filter functionality for products.

    This test ensures that when the 'no_categories' filter is applied to the
    Product queryset, it returns only the products without any associated
    categories, and excludes those with associated categories.
    """
    # create products with categories and without
    product_with_category = ProductFactory(
        name="With category", categories=[category]
    )
    product_with_category.categories.add(category)
    product_without_category = ProductFactory(name="Without category")

    # apply filter 'no_categories'
    no_categories_filter = ProductFilter(
        {"uncategorized": True}, queryset=Product.objects.all()
    )

    # Check that a product without a category is returned by the filter
    assert product_without_category in no_categories_filter.qs

    # Check that a product with a category is not returned by the filter
    assert product_with_category not in no_categories_filter.qs
