import os.path
from abc import ABC, abstractmethod

import pytest
from django.urls import reverse
from rest_framework import status

from apps.products.models import (
    Product,
    ProductImage,
    ProductSize,
    Size,
    Image,
)
from apps.products.tests.factories import ProductFactory


class ProductRelatedViewSetTestBase(ABC):
    NON_EXISTENT_ID = 9999

    @pytest.fixture(autouse=True)
    def setup_product(self, products_with_associations):
        self.products = products_with_associations
        self.product = self.products[5]
        self.target_item = self.get_target_item(self.product)
        self.url_list = self.build_url(product_id=self.product.id)
        self.url_detail = self.build_url(
            product_id=self.product.id, item_id=self.target_item.id
        )
        self.url_list_not_found = self.build_url(
            product_id=self.NON_EXISTENT_ID
        )
        self.url_detail_not_found_item = self.build_url(
            product_id=self.product.id, item_id=self.NON_EXISTENT_ID
        )
        self.url_detail_not_found_product = self.build_url(
            product_id=self.NON_EXISTENT_ID, item_id=self.target_item.id
        )

    @abstractmethod
    def get_target_item(self, product):
        pass

    def build_url(self, product_id, item_id=None):
        base_name = self.get_url_name()
        detail_or_list = "detail" if item_id else "list"
        kwargs = {"product_id": product_id}
        if item_id:
            kwargs[self.get_item_id_name()] = item_id
        return reverse(f"products:{base_name}-{detail_or_list}", kwargs=kwargs)

    @abstractmethod
    def get_url_name(self):
        pass

    @abstractmethod
    def get_item_id_name(self):
        pass


@pytest.mark.django_db
class TestProductImagesViewSet(ProductRelatedViewSetTestBase):
    def get_target_item(self, product):
        return product.images.all()[2]

    def get_url_name(self):
        return "productimages"

    def get_item_id_name(self):
        return "image_id"

    def test_list(self, api_client):
        """
        Test that the API endpoint for listing product images returns the
        correct status code and the correct number of images.
        """
        response = api_client.get(self.url_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == self.product.images.count()

    def test_list_returns_404_when_product_not_found(self, api_client):
        """
        Test that the API endpoint for listing product images returns a 404
        status code when the product ID does not exist.
        """

        response = api_client.get(self.url_list_not_found)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_returns_empty(
        self, api_client, products_without_associations
    ):
        """
        Test that the API endpoint for listing product images returns an empty
        list when the product has no images.
        """
        product = products_without_associations[5]

        response = api_client.get(self.build_url(product_id=product.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_create(self, api_client, image_no_save_file):
        """
        Test that the API endpoint for creating a product image returns the
        correct status code and that the image is successfully created.
        """
        image_file = image_no_save_file.build().img
        data = {"new_image": image_file}
        response = api_client.post(self.url_list, data)

        db_image_filename = os.path.basename(
            self.product.images.get(pk=response.data["image"]["id"]).img.name
        )
        uploaded_image_filename = data["new_image"].name
        assert response.status_code == status.HTTP_201_CREATED
        assert db_image_filename == uploaded_image_filename

    def test_create_returns_404_when_product_not_found(
        self, api_client, image_no_save_file
    ):
        """
        Test that the API endpoint for creating a product image returns the
        returns a 404 status code when the product ID does not exist.
        """
        image_file = image_no_save_file.build().img
        data = {"new_image": image_file}
        response = api_client.post(self.url_list_not_found, data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve(self, api_client):
        """
        Test that the API endpoint for retrieving a product image returns the
        correct status code and the correct image.
        """
        response = api_client.get(self.url_detail)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["image"]["id"] == self.target_item.id

    @pytest.mark.parametrize(
        "url", ["url_detail_not_found_item", "url_detail_not_found_product"]
    )
    def test_retrieve_returns_404_when_param_not_found(self, api_client, url):
        """
        Test that the API endpoint for retrieving a product image returns a 404
        status code when the image ID or product ID does not exist.
        """
        response = api_client.get(getattr(self, url))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update(self, api_client, image_no_save_file):
        """
        Test that the API endpoint for partially updating a product image
        returns the correct status code and updates the image correctly.
        """
        image_file = image_no_save_file.build().img
        data = {"new_image": image_file}
        response = api_client.patch(self.url_detail, data)
        db_image_filename = os.path.basename(
            self.product.images.get(pk=response.data["image"]["id"]).img.name
        )
        uploaded_image_filename = data["new_image"].name
        assert response.status_code == status.HTTP_200_OK
        assert db_image_filename == uploaded_image_filename

    @pytest.mark.parametrize(
        "url", ["url_detail_not_found_item", "url_detail_not_found_product"]
    )
    def test_partial_update_returns_404_when_param_not_found(
        self, api_client, image_no_save_file, url
    ):
        """
        Test that the API endpoint for partially updating
        a product image returns a 404 status code when the image ID
        or product ID does not exist.
        """
        image_file = image_no_save_file.build().img
        data = {"new_image": image_file}

        response = api_client.patch(getattr(self, url), data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_destroy(self, api_client, image_no_save_file):
        """
        Test that the API endpoint for deleting a product image returns the
        correct status code and successfully removes the association
        between the image and the product.
        """
        initial_image_count = self.product.images.count()
        response = api_client.delete(self.url_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not self.product.images.filter(pk=self.target_item.id)
        final_image_count = self.product.images.count()
        assert final_image_count == initial_image_count - 1

    @pytest.mark.parametrize(
        "url", ["url_detail_not_found_item", "url_detail_not_found_product"]
    )
    def test_destroy_returns_404_when_param_not_found(self, api_client, url):
        """
        Test that the API endpoint for deleting a product image returns a 404
        status code when the image ID or product ID does not exist.
        """

        response = api_client.delete(getattr(self, url))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize("is_preview", [True, False])
    def test_update_preview_status(self, api_client, is_preview):
        """
        Test that the API endpoint for updating the preview status of a product
        image returns the correct status code
        and updates the preview status correctly.
        """
        data = {"is_preview": is_preview}
        response = api_client.patch(self.url_detail, data)
        assert response.status_code == status.HTTP_200_OK
        assert (
            ProductImage.objects.get(
                product=self.product, image=self.target_item
            ).is_preview
            is is_preview
        )

    def test_invalid_image_file(self, api_client):
        """
        Test that the API endpoint returns the correct status code
        when an invalid image file is provided.
        """

        data = {"new_image": "invalid_image_file"}
        response = api_client.patch(self.url_detail, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestProductViewSet:
    def test_create_product(self, api_client, product_serializer_write_data):
        url = reverse("products:product-list")
        response = api_client.post(url, product_serializer_write_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == product_serializer_write_data["name"]
        assert Product.objects.filter(pk=response.data["id"]).exists()
        product = Product.objects.get(pk=response.data["id"])
        assert product.name == product_serializer_write_data["name"]
        assert product.images.count() == len(
            product_serializer_write_data["images_ids"]
        )

    def test_list_products(self, api_client):
        ProductFactory.create_batch(5)
        url = reverse("products:product-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Product.objects.all().count() == len(response.data)

    def test_retrieve_product(self, api_client, product):
        url = reverse("products:product-detail", kwargs={"pk": product.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == product.id

    def test_update_product(
        self, api_client, product, product_serializer_write_data
    ):
        url = reverse("products:product-detail", kwargs={"pk": product.id})
        response = api_client.put(url, product_serializer_write_data)
        product.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert product.name == product_serializer_write_data["name"]

    def test_partial_update_product(self, api_client, product):
        url = reverse("products:product-detail", kwargs={"pk": product.id})
        partial_update_data = {"name": "New product name"}
        response = api_client.patch(url, partial_update_data)
        product.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert product.name == partial_update_data["name"]

    def test_destroy_product(self, api_client, product):
        url = reverse("products:product-detail", kwargs={"pk": product.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(pk=product.id).exists()
