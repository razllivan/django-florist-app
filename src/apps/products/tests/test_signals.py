import os

import pytest
from django.conf import settings

from apps.products.tests.factories import CategoryFactory, ImageFactory


@pytest.mark.django_db
def test_add_parent_categories_on_add(product):
    """
    Test if adding a child category to a product
    also adds its parent category and grandparent catergory.
    """
    # Create thr categories
    category_grandparent = CategoryFactory()
    category_parent = CategoryFactory(parent_category=category_grandparent)
    category_child = CategoryFactory(parent_category=category_parent)

    # Add the child category to product
    product.categories.add(category_child)
    product.refresh_from_db()

    assert category_child in product.categories.all()
    assert category_parent in product.categories.all()
    assert category_grandparent in product.categories.all()


@pytest.mark.django_db
def test_delete_image_file_on_instance_delete(image):
    """
    Test that the image file is deleted from the filesystem when the
    Image model instance's file field is deleted.
    """
    image_path = os.path.join(settings.MEDIA_ROOT, image.img.name)

    # Check that the file exists in the filesystem
    assert os.path.isfile(image_path)

    # Delete the image instance
    image.delete()

    # Check that the file is also deleted from the filesystem
    assert not os.path.isfile(image_path)


@pytest.mark.django_db
def test_delete_image_file_on_instance_change(image):
    """
    Test that the image file is deleted from the filesystem when the
    Image model instance's file field is updated.
    """
    old_image_path = os.path.join(settings.MEDIA_ROOT, image.img.name)

    # Check that the file exists in the filesystem
    assert os.path.isfile(old_image_path)

    new_image = ImageFactory.build()
    image.img = new_image.img
    image.save()

    assert not os.path.isfile(old_image_path)
    image.delete()
