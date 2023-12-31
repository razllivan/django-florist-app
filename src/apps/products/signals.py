import os

from django.db.models.signals import m2m_changed, post_delete, pre_save
from django.dispatch import receiver

from apps.products.models import Image, Product


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


@receiver(post_delete, sender=Image)
def delete_image_file_on_instance_delete(sender, instance, **kwargs):
    """
    Deletes old image file from filesystem
    when corresponding `Image` object is deleted.
    """
    if instance.img and os.path.isfile(instance.img.path):
        instance.img.delete(save=False)


@receiver(pre_save, sender=Image)
def delete_image_file_on_instance_change(sender, instance, **kwargs):
    """
    Deletes the old image file from filesystem when Image instance is updated.
    """
    # Exit if Image instance is new and not saved yet
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).img
    except sender.DoesNotExist:
        return False

    new_file = instance.img
    if old_file != new_file and os.path.isfile(old_file.path):
        old_file.delete(save=False)
