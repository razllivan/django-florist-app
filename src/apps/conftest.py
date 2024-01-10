import pytest
from rest_framework.test import APIClient

from apps.products.tests.factories import (
    CategoryFactory,
    ImageFactory,
    ProductFactory,
    ProductImageFactory,
    ProductSizeFactory,
    SizeFactory,
)


@pytest.fixture()
def mock_image_save(monkeypatch):
    """
    A pytest fixture that mocks the 'save' method of
    Django's FileSystemStorage. Used in tests to avoid actual
    image file creation.
    """

    def mock_save(_, name, *args, **kwargs):
        return f"path/to/{name}"

    monkeypatch.setattr(
        "django.core.files.storage.FileSystemStorage.save", mock_save
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product(db):
    return ProductFactory()


@pytest.fixture
def products_without_associations(db):
    return ProductFactory.create_batch(10)


@pytest.fixture
def products_with_associations(db, image_no_save_file):
    products = ProductFactory.create_batch(10)
    for product in products:
        images = image_no_save_file.create_batch(4)
        product.images.add(*images)

        categories = CategoryFactory.create_batch(4)
        product.categories.add(*categories)

        ProductSizeFactory.create_batch(4, product=product)

    return products


@pytest.fixture
def product_serializer_write_data(db, image_no_save_file) -> dict:
    """
    Provides a dictionary of data for creating or updating a Product instance
    via the ProductSerializer.
    Includes fields necessary for writing:
    categories_ids, sizes_ids, and images_ids.

    Use this fixture when testing the ProductSerializer
    with write operations.
    """
    product = ProductFactory.build()

    return {
        "name": product.name,
        "description": product.description,
    }


@pytest.fixture
def image(db):
    return ImageFactory()


@pytest.fixture
def image_no_save_file(db, mock_image_save):
    return ImageFactory


@pytest.fixture
def product_image_no_save_file(db, mock_image_save):
    return ProductImageFactory()


@pytest.fixture
def category(db):
    return CategoryFactory()


@pytest.fixture
def product_size_serializer_write_data(db) -> dict:
    """
    Provides a dictionary of data for updating a Product instance
    via the ProductSizeSerializer.


    Use this fixture when testing the ProductSizeSerializer
    with write operations.
    """
    product_size = ProductSizeFactory.build()
    return {
        "price": product_size.price,
        "is_active": True,
    }


@pytest.fixture
def size(db):
    return SizeFactory()


@pytest.fixture
def product_image_serializer_write_data(db) -> dict:
    """
    Provides a dictionary of data for updating a Product instance
    via the ProductImageSerializer.


    Use this fixture when testing the ProductSizeSerializer
    with write operations.
    """
    product_image = ProductImageFactory.build()
    return {"is_preview": product_image.is_preview}
