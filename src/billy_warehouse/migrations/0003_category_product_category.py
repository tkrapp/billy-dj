# Generated by Django 4.0 on 2021-12-11 21:34

from django.db import migrations, models
import django.db.models.deletion


CATEGORY_UNKNOWN = "Unknown"


def populate_category(apps, schema_editor):
    """
    Populate category field
    """
    db_alias = schema_editor.connection.alias
    Category = apps.get_model("billy_warehouse", "Category")
    Product = apps.get_model("billy_warehouse", "Product")

    cat_unknown = Category.objects.using(db_alias).get(name=CATEGORY_UNKNOWN)
    Product.objects.using(db_alias).filter(category=None).update(category=cat_unknown)


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

    dependencies = [
        ("billy_warehouse", "0002_stock"),
    ]

    operations = [
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
            code=add_default_category, reverse_code=remove_default_category
        ),
        migrations.RunPython(
            code=populate_category, reverse_code=migrations.RunPython.noop
        ),
    ]
