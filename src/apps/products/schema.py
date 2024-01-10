from drf_spectacular.utils import extend_schema


class ProductSizesSchema:
    def list(self):
        return extend_schema(
            summary="Get all sizes related to the product",
            description="Get all sizes related to the product",
        )

    def create(self):
        return extend_schema(
            summary="Add size to product and fill associated fields",
            description="Add size to product and fill associated fields",
        )

    def retrieve(self):
        return extend_schema(
            summary="Get info about a specific size and its association "
            "info with a product",
            description="Get info about a specific size and its association "
            "info with a product",
        )

    def partial_update(self):
        return extend_schema(
            summary="Update size information about association with a product",
            description="""Updates only size information that belongs
            to a specific product.
            <br>
            If you need to change information about
            the size itself, use the `/api/sizes` endpoint""",
        )

    def destroy(self):
        return extend_schema(
            summary="Remove product size",
            description="""Remove only association between size and product.
            <br>
            To delete the size itself you need to use the `/api/sizes`
            endpoint""",
        )


class ProductImagesSchema:
    def list(self):
        return extend_schema(
            summary="Get all images related to the product",
            description="Get all images related to the product",
        )

    def create(self):
        return extend_schema(
            summary="Add image to product and fill associated fields",
            description="Add image to product and fill associated fields",
        )

    def retrieve(self):
        return extend_schema(
            summary="Get info about a specific image and its association "
            "info with a product",
            description="Get info about a specific image and its association "
            "info with a product",
        )

    def partial_update(self):
        return extend_schema(
            summary="Update image information about association "
            "with a product",
            description="""Updates only image information that belongs
            to a specific product.
            <br>
            If you need to change information about
            the image itself, use the `/api/images` endpoint""",
        )

    def destroy(self):
        return extend_schema(
            summary="Remove product image",
            description="""Remove only association between image and product.
            <br>
            To delete the image itself you need to use the `/api/images`
            endpoint""",
        )


class ProductCategoriesSchema:
    def list(self):
        return extend_schema(
            summary="Get all categories related to the product",
            description="Get all categories related to the product",
        )

    def create(self):
        return extend_schema(
            summary="Add category to product",
            description="Add category to product",
        )

    def destroy(self):
        return extend_schema(
            summary="Remove product image",
            description="""Remove only association between image and product.
            <br>
            To delete the image itself you need to use the `/api/images`
            endpoint""",
        )
