# Generated by Django 4.0 on 2021-12-11 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billy_invoice', '0005_alter_invoiceitem_price_per_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceitem',
            old_name='price_per_unit',
            new_name='netto_price_per_unit',
        ),
    ]
