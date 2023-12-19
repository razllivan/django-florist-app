import factory
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

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return
        # Add the iterable of categories using bulk addition
        self.categories.add(*extracted)


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = SubFactory(ProductFactory)
    image = SubFactory(ImageFactory)
