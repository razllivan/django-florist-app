from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.products.models import Product


@receiver(m2m_changed, sender=Product.categories.through)
def add_parent_categories_on_add(sender, instance, action, **kwargs):
    """
    Handle the signal fired when the many-to-many relationship between
    a Product and its Categories is changed. Specifically, when a category
    is added to a product, all the parent categories of that category are
    also added to the product. This continues up the category hierarchy
    until all parent categories have been added.

    Args:
        sender: The model class.
        instance: The actual instance of the model that the signal was
                  performed on.
        action: A string indicating the type of update that was done.
    """
    if action == "post_add":
        new_parents = set()
        categories = instance.categories.all()
        for category in categories:
            parent = category.parent_category
            while parent is not None:
                if parent not in categories:
                    new_parents.add(parent)
                parent = parent.parent_category
        instance.categories.add(*new_parents)
