import os

from autoslug import AutoSlugField
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=200, help_text="The name of the category."
    )
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        db_index=True,
        always_update=True,
        help_text="Unique slug generated from the category name for URL.",
    )
    is_active = models.BooleanField(
        default=True, db_index=True, help_text="Hide category from the catalog"
    )
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="child_categories",
        help_text="id to the parent category for hierarchical structuring.",
    )

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50, help_text="The name of the size.")

    def __str__(self):
        return self.name


class Image(models.Model):
    img = models.ImageField(upload_to="images/")
    size_description = models.CharField(
        max_length=100,
        blank=True,
        help_text="Product size info in the picture",
    )

    def __str__(self):
        return os.path.basename(self.img.name)


class Product(models.Model):
    name = models.CharField(
        max_length=200, help_text="The name of the product"
    )
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        db_index=True,
        always_update=True,
        help_text="Unique slug generated from the category name for URL.",
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Hide product from the catalog",
    )
    description = models.TextField(
        blank=True, help_text="A description of the product"
    )
    is_archived = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Automatically marked as archived when deleted if "
        "referenced by an order",
    )
    categories = models.ManyToManyField(Category, blank=True)
    sizes = models.ManyToManyField(Size, through="ProductSize", blank=True)
    images = models.ManyToManyField(Image, through="ProductImage", blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    is_preview = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Sets the image as a preview for the product",
    )

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
    price = models.PositiveIntegerField(
        help_text="The price for this product in this size"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Hide size for this product from the catalog",
    )
