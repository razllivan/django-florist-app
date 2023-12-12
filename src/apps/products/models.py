from autoslug import AutoSlugField
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from="name", unique=True, db_index=True, always_update=True
    )
    is_active = models.BooleanField(default=True)
    parent_category = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    @staticmethod
    def get_default_category():
        return Category.objects.get_or_create(
            name="Без категории", is_active=False
        )[0]
