# Generated by Django 4.0 on 2021-12-11 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "billy_warehouse",
            "0005_alter_category_options_alter_product_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="create_timestamp",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Create timestamp"
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="update_timestamp",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Update timestamp"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="create_timestamp",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Create timestamp"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="update_timestamp",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Update timestamp"
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="create_timestamp",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Create timestamp"
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="update_timestamp",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Update timestamp"
            ),
        ),
        migrations.AddField(
            model_name="vendor",
            name="create_timestamp",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Create timestamp"
            ),
        ),
        migrations.AddField(
            model_name="vendor",
            name="update_timestamp",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Update timestamp"
            ),
        ),
    ]
