# Generated by Django 4.2.8 on 2023-12-20 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_alter_product_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="parent_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="child_categories",
                to="products.category",
            ),
        ),
    ]
