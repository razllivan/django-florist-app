from rest_framework import mixins
from rest_framework.generics import get_object_or_404

from apps.products.models import Product


class ListProductMixin(mixins.ListModelMixin):
    """
    A mixin for listing products.

        This mixin adds a check to ensure that the product with the
    specified product_id exists before listing the products. It is added
    to avoid returning an empty dictionary in the response and 200
    status code if the product is not found.
        If the product is not
    found, a 404 status code will be returned instead of 200.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset and "product_id" in self.kwargs:
            product_id = self.kwargs.get("product_id")
            get_object_or_404(Product, pk=product_id)
        return super().list(request, *args, **kwargs)


class ProductRelationsMixin:
    """
    A mixin to provide common query functionalities for product-related views.

        This mixin expects a Django model to be specified in the 'model'
    attribute by subclasses. It provides a method to retrieve a queryset
    filtered by a product ID, which is expected to be provided in the view's
    keyword arguments (`self.kwargs`).
        It also handles the case where the
    view is being used to generate a Swagger schema by returning an empty
    queryset.

    Attributes:
        model: The Django model class associated with the product-related data.
        Subclasses must provide this attribute.

    Raises:
        AttributeError: If a subclass does not specify the 'model' attribute.
    """

    model = None

    def __init__(self, *args, **kwargs):
        if not self.model:
            raise AttributeError(
                "Subclasses must specify the 'model' attribute"
            )
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # Return a fake queryset for schema generation
            return self.model.objects.none()
        product_id = self.kwargs["product_id"]
        return self.model.objects.filter(product_id=product_id)


class PerformCreateProductMixin:
    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(product=product)


class CreateMixin(mixins.CreateModelMixin):
    """
    A mixin that allows specifying a separate serializer for the create method.

    Attributes:
        serializer_create_class (Serializer): The serializer class to be used
         for creating objects.

    Raises:
        AttributeError: If the 'serializer_create_class' attribute is not
         specified in subclasses.
    """

    serializer_create_class = None

    def __init__(self, *args, **kwargs):
        if not self.serializer_create_class:
            raise AttributeError(
                "Subclasses must specify the 'serializer_create_class' "
                "attribute"
            )
        super().__init__(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create":
            return self.serializer_create_class
        return super().get_serializer_class()
