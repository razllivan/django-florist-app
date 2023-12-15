import pytest

from apps.products.models import Category
from apps.products.tests.factories import ProductFactory, ProductImageFactory


@pytest.mark.django_db
def test_get_default_category():
    """
    Tests `get_default_category` method from `Category` model. The function
    checks that the default category is inactive, named "Без категории",
    and does not create a new category but reuses the existing one.
    """
    category1 = Category.get_default_category()
    assert category1.name == "Без категории"
    assert not category1.is_active

    category2 = Category.get_default_category()
    assert category1.id == category2.id


@pytest.mark.django_db
def test_product_image_save(mock_image_save):
    """
    Test the 'preview' functionality of the `ProductImage` model.
    It asserts that only one image per product can be set as 'preview'.
    The `mock_image_save` parameter is a mock object for image saving.
    """
    product = ProductFactory()
    image1 = ProductImageFactory(product=product, is_preview=True)
    image1.save()
    image1.refresh_from_db()
    assert image1.is_preview

    image2 = ProductImageFactory(product=product, is_preview=True)
    image1.refresh_from_db()

    assert not image1.is_preview
    assert image2.is_preview
