# Generated by Django 4.0 on 2021-12-11 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("billy_warehouse", "0004_alter_product_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "Product", "verbose_name_plural": "Products"},
        ),
        migrations.AlterModelOptions(
            name="stock",
            options={"verbose_name": "Stock", "verbose_name_plural": "Stocks"},
        ),
        migrations.AlterModelOptions(
            name="vendor",
            options={"verbose_name": "Vendor", "verbose_name_plural": "Vendors"},
        ),
    ]
