# Generated by Django 4.2.8 on 2023-12-18 19:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_remove_product_category_product_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="category",
            new_name="categories",
        ),
    ]
