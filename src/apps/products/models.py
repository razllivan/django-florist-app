import os

from autoslug import AutoSlugField
from django.db import models


class CatalogItemBase(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from="name", unique=True, db_index=True, always_update=True
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class Category(CatalogItemBase):
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="child_categories",
    )

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    img = models.ImageField(upload_to="images/")

    def __str__(self):
        return os.path.basename(self.img.name)


class Product(CatalogItemBase):
    description = models.TextField(blank=True)
    size_description = models.CharField(max_length=100, blank=True)
    is_archived = models.BooleanField(default=False, db_index=True)
    categories = models.ManyToManyField(Category, blank=True)
    sizes = models.ManyToManyField(Size, through="ProductSize", blank=True)
    images = models.ManyToManyField(Image, through="ProductImage", blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    is_preview = models.BooleanField(default=False, db_index=True)

    def save(self, *args, **kwargs):
        """
        If the instance is a preview,
        it updates the preview status of all other previews of the same
        product to False.
        """
        if self.is_preview:
            self.__class__.objects.filter(
                product=self.product, is_preview=True
            ).update(is_preview=False)

        super().save(*args, **kwargs)


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True, db_index=True)
