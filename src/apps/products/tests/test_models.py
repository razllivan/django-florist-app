import pytest

from apps.products.models import Category


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
