import os.path

import pytest
from django.urls import reverse
from rest_framework import status

from apps.products.models import ProductImage


@pytest.mark.django_db
class TestProductImagesViewSet:
    def test_list_product_images(
        self, api_client, product, product_image_no_save_file
    ):
        """
        Test that the API endpoint for listing product images returns the
        correct status code and the correct number of images.
        """
        url = reverse(
            "products:productimages-list", kwargs={"product_id": product.id}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            len(response.data)
            == ProductImage.objects.filter(product=product).count()
        )

    def test_create_product_image(
        self, api_client, product, image_no_save_file
    ):
        """
        Test that the API endpoint for creating a product image returns the
        correct status code and that the image is successfully created.
        """
        url = reverse(
            "products:productimages-list", kwargs={"product_id": product.id}
        )
        image_file = image_no_save_file.build().img
        data = {"new_image": image_file}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert ProductImage.objects.filter(product=product).exists()

    def test_retrieve_product_image(
        self, api_client, product_image_no_save_file
    ):
        """
        Test that the API endpoint for retrieving a product image returns the
        correct status code and the correct image.
        """
        url = reverse(
            "products:productimages-detail",
            kwargs={
                "product_id": product_image_no_save_file.product.id,
                "pk": product_image_no_save_file.image.id,
            },
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["image"]["id"] == product_image_no_save_file.image.id
        )

    def test_partial_update_product_image(
        self, api_client, product_image_no_save_file, image_no_save_file
    ):
        """
        Test that the API endpoint for partially updating a product image
        returns the correct status code and updates the image correctly.
        """
        url = reverse(
            "products:productimages-detail",
            kwargs={
                "product_id": product_image_no_save_file.product.id,
                "pk": product_image_no_save_file.image.id,
            },
        )
        image_file = image_no_save_file.build().img
        data = {"new_image": image_file}
        response = api_client.patch(url, data)
        product_image_no_save_file.refresh_from_db()
        db_image_filename = os.path.basename(
            product_image_no_save_file.image.img.name
        )
        uploaded_image_filename = data["new_image"].name
        assert response.status_code == status.HTTP_200_OK
        assert db_image_filename == uploaded_image_filename

    def test_destroy_product_image(
        self, api_client, product_image_no_save_file
    ):
        """
        Test that the API endpoint for deleting a product image returns the
        correct status code and deletes the image successfully.
        """
        url = reverse(
            "products:productimages-detail",
            kwargs={
                "product_id": product_image_no_save_file.product.id,
                "pk": product_image_no_save_file.image.id,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductImage.objects.filter(
            id=product_image_no_save_file.id
        ).exists()

    def test_update_preview_status(
        self, api_client, product_image_no_save_file
    ):
        """
        Test that the API endpoint for updating the preview status of a product
        image returns the correct status code
        and updates the preview status correctly.
        """
        url = reverse(
            "products:productimages-detail",
            kwargs={
                "product_id": product_image_no_save_file.product.id,
                "pk": product_image_no_save_file.image.id,
            },
        )
        data = {"is_preview": True}
        response = api_client.patch(url, data)
        product_image_no_save_file.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert product_image_no_save_file.is_preview is True

    def test_invalid_image_file(self, api_client, product_image_no_save_file):
        """
        Test that the API endpoint returns the correct status code
        when an invalid image file is provided.
        """
        url = reverse(
            "products:productimages-detail",
            kwargs={
                "product_id": product_image_no_save_file.product.id,
                "pk": product_image_no_save_file.image.id,
            },
        )
        data = {"new_image": "invalid_image_file"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
