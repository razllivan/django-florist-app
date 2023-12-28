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
