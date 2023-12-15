from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory, ImageField

from apps.products.models import Category, Image, Product, ProductImage


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Sequence(lambda n: f"category-{n}")


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    img = ImageField(filename=Sequence(lambda n: f"image-{n}.jpg"))


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    description = Faker("text")
    category = SubFactory(CategoryFactory)


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = SubFactory(ProductFactory)
    image = SubFactory(ImageFactory)
