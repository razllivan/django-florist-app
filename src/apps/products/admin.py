from django.contrib import admin

from apps.products.models import Category, Image, Product, Size

admin.site.register([Category, Image, Size])


class SizesInline(admin.TabularInline):
    model = Product.sizes.through


class ImagesInline(admin.TabularInline):
    model = Product.images.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        SizesInline,
        ImagesInline,
    ]
    exclude = ["sizes", "images"]
