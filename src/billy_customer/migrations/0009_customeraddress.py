# Generated by Django 4.0 on 2021-12-14 04:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("billy_customer", "0008_remove_customer_addresses"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomerAddress",
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
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("hidden", models.BooleanField(default=False, verbose_name="Hidden")),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="billy_customer.address",
                        verbose_name="Address",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="billy_customer.customer",
                        verbose_name="Customer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]