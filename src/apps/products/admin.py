from django.contrib import admin

from apps.products.models import Category, Image, Product, Size

admin.site.register([Category, Image, Size])


class SizesInline(admin.TabularInline):
    model = Product.sizes.through


class ImagesInline(admin.TabularInline):
    model = Product.images.through


class CategoryInline(admin.TabularInline):
    model = Product.categories.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "slug",
        "is_active",
        "is_archived",
        "description",
    )
    inlines = [
        CategoryInline,
        SizesInline,
        ImagesInline,
    ]
    exclude = ["sizes", "images", "categories"]
    readonly_fields = (
        "slug",
        "id",
    )
