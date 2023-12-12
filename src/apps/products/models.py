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


class Size(models.Model):
    name = models.CharField(max_length=50)


class Image(models.Model):
    img = models.ImageField(upload_to="images/")


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    size_description = models.CharField(max_length=100, blank=True, null=True)
    slug = AutoSlugField(
        populate_from="name", unique=True, db_index=True, always_update=True
    )
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET(Category.get_default_category)
    )
    sizes = models.ManyToManyField(Size, through="ProductSize")
    images = models.ManyToManyField(Image, through="ProductImage")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    is_preview = models.BooleanField(default=False)
