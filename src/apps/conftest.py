import pytest
from rest_framework.test import APIClient

from apps.products.tests.factories import (
    CategoryFactory,
    ImageFactory,
    ProductFactory,
    ProductImageFactory,
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
def products_with_images(db, image_no_save_file):
    products = ProductFactory.create_batch(10)
    for product in products:
        images = image_no_save_file.create_batch(4)
        product.images.add(*images)
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
    categories = CategoryFactory.create_batch(2)
    images = image_no_save_file.create_batch(3)

    return {
        "name": product.name,
        "description": product.description,
        "categories_ids": [category.id for category in categories],
        "images_ids": [image.id for image in images],
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
