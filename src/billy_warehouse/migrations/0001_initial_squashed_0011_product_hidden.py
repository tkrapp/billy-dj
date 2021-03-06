# Generated by Django 4.0 on 2021-12-16 21:00

from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


CATEGORY_UNKNOWN = "Unknown"


def add_default_category(apps, schema_editor):
    """
    Add a default category
    """
    db_alias = schema_editor.connection.alias
    Category = apps.get_model("billy_warehouse", "Category")

    Category.objects.using(db_alias).create(name=CATEGORY_UNKNOWN)


def remove_default_category(apps, schema_editor):
    """
    Remove the default category
    """
    db_alias = schema_editor.connection.alias
    Category = apps.get_model("billy_warehouse", "Category")

    Category.objects.using(db_alias).filter(name=CATEGORY_UNKNOWN).delete()


class Migration(migrations.Migration):

    replaces = [
        ("billy_warehouse", "0001_initial"),
        ("billy_warehouse", "0002_stock"),
        ("billy_warehouse", "0003_category_product_category"),
        ("billy_warehouse", "0004_alter_product_category"),
        (
            "billy_warehouse",
            "0005_alter_category_options_alter_product_options_and_more",
        ),
        (
            "billy_warehouse",
            "0006_category_create_timestamp_category_update_timestamp_and_more",
        ),
        ("billy_warehouse", "0007_remove_category_create_timestamp_and_more"),
        ("billy_warehouse", "0008_alter_product_price"),
        ("billy_warehouse", "0009_rename_price_product_netto_price"),
        ("billy_warehouse", "0010_alter_product_netto_price"),
        ("billy_warehouse", "0011_product_hidden"),
    ]

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Name"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="Name"),
                ),
                ("price", models.PositiveBigIntegerField(verbose_name="Price")),
                ("details", models.JSONField(verbose_name="Details")),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="billy_warehouse.vendor",
                        verbose_name="Vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveSmallIntegerField(verbose_name="Quantity")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="billy_warehouse.product",
                        verbose_name="Product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Name"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="billy_warehouse.category",
                verbose_name="Category",
            ),
        ),
        migrations.RunPython(
            code=add_default_category,
            reverse_code=remove_default_category,
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="billy_warehouse.category",
                verbose_name="Category",
            ),
        ),
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
        migrations.AddField(
            model_name="category",
            name="created",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="created",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="modified",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="modified",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="created",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="created",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="modified",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="modified",
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="created",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="created",
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="modified",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="modified",
            ),
        ),
        migrations.AddField(
            model_name="vendor",
            name="created",
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="created",
            ),
        ),
        migrations.AddField(
            model_name="vendor",
            name="modified",
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="modified",
            ),
        ),
        migrations.RenameField(
            model_name="product",
            old_name="price",
            new_name="netto_price",
        ),
        migrations.AlterField(
            model_name="product",
            name="netto_price",
            field=models.PositiveBigIntegerField(verbose_name="Price (in Cents)"),
        ),
        migrations.AlterField(
            model_name="product",
            name="netto_price",
            field=models.PositiveBigIntegerField(verbose_name="Netto price (in Cents)"),
        ),
        migrations.AddField(
            model_name="product",
            name="hidden",
            field=models.BooleanField(default=False, verbose_name="Hidden"),
        ),
    ]
