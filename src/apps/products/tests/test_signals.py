import pytest

from apps.products.tests.factories import CategoryFactory, ProductFactory


@pytest.mark.django_db
def test_add_parent_categories_on_add():
    """
    Test if adding a child category to a product
    also adds its parent category and grandparent catergory.
    """
    # Create thr categories
    category_grandparent = CategoryFactory()
    category_parent = CategoryFactory(parent_category=category_grandparent)
    category_child = CategoryFactory(parent_category=category_parent)

    # Create the product and add the child category
    product = ProductFactory()
    product.categories.add(category_child)
    product.refresh_from_db()

    assert category_child in product.categories.all()
    assert category_parent in product.categories.all()
    assert category_grandparent in product.categories.all()
