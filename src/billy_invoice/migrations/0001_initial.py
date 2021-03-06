# Generated by Django 4.0 on 2021-12-10 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("billy_customer", "0001_initial"),
        ("billy_warehouse", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
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
                    "invoice_number",
                    models.CharField(max_length=20, verbose_name="Invoice number"),
                ),
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
        ),
        migrations.CreateModel(
            name="InvoiceItem",
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
                ("quantity", models.PositiveBigIntegerField(verbose_name="Quantity")),
                (
                    "price_per_unit",
                    models.PositiveBigIntegerField(verbose_name="Price per unit"),
                ),
                (
                    "vat_rate",
                    models.PositiveSmallIntegerField(
                        choices=[(19, "Nineteen"), (7, "Seven")],
                        verbose_name="VAT rate",
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="billy_invoice.invoice",
                        verbose_name="Invoice",
                    ),
                ),
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
    ]
