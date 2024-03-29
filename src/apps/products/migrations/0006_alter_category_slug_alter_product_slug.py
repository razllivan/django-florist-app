# Generated by Django 4.2.8 on 2024-01-12 15:20

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_alter_category_slug_alter_product_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                blank=True,
                editable=True,
                help_text="Automatically generates a unique slug from the name when creating the object for URL purposes. The slug remains unchanged even if the name is modified, and it needs to be updated manually if necessary.",
                populate_from="name",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                blank=True,
                editable=True,
                help_text="Automatically generates a unique slug from the name when creating the object for URL purposes. The slug remains unchanged even if the name is modified, and it needs to be updated manually if necessary.",
                populate_from="name",
                unique=True,
            ),
        ),
    ]
