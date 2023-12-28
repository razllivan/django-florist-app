import pytest

from apps.products.tests.factories import ProductImageFactory


@pytest.mark.django_db
def test_only_one_image_per_product_as_preview(mock_image_save, product):
    """
    Test the 'preview' functionality of the `ProductImage` model.
    It asserts that only one image per product can be set as 'preview'.
    The `mock_image_save` parameter is a mock object for image saving.
    """
    image1 = ProductImageFactory(product=product, is_preview=True)
    assert image1.is_preview

    image2 = ProductImageFactory(product=product, is_preview=True)
    image1.refresh_from_db()

    assert image1.is_preview is False
    assert image2.is_preview
