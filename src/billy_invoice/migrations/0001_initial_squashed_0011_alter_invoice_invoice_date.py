# Generated by Django 4.0 on 2021-12-16 20:59

import billy_invoice.models
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    replaces = [
        ("billy_invoice", "0001_initial"),
        ("billy_invoice", "0002_alter_invoice_options_alter_invoiceitem_options"),
        (
            "billy_invoice",
            "0003_invoice_create_timestamp_invoice_update_timestamp_and_more",
        ),
        ("billy_invoice", "0004_remove_invoice_create_timestamp_and_more"),
        ("billy_invoice", "0005_alter_invoiceitem_price_per_unit"),
        (
            "billy_invoice",
            "0006_rename_price_per_unit_invoiceitem_netto_price_per_unit",
        ),
        ("billy_invoice", "0007_alter_invoiceitem_netto_price_per_unit"),
        ("billy_invoice", "0008_invoice_invoice_date"),
        ("billy_invoice", "0009_alter_invoice_invoice_date"),
        ("billy_invoice", "0010_alter_invoice_invoice_date"),
        ("billy_invoice", "0011_alter_invoice_invoice_date"),
    ]

    dependencies = [
        ("billy_warehouse", "0001_initial"),
        ("billy_customer", "0001_initial"),
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
                (
                    "invoice_date",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="Invoice date"
                    ),
                ),
            ],
            options={
                "verbose_name": "Invoice",
                "verbose_name_plural": "Invoices",
            },
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
                    "netto_price_per_unit",
                    models.PositiveBigIntegerField(
                        verbose_name="Netto price per unit (in Cents)"
                    ),
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
            ],
            options={
                "verbose_name": "Invoice item",
                "verbose_name_plural": "Invoice items",
            },
        ),
        migrations.AlterField(
            model_name="invoice",
            name="invoice_date",
            field=models.DateField(auto_now_add=True, verbose_name="Invoice date"),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="invoice_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Invoice date"
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="invoice_date",
            field=models.DateField(
                default=billy_invoice.models.today, verbose_name="Invoice date"
            ),
        ),
    ]
