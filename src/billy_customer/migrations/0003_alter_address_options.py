# Generated by Django 4.0 on 2021-12-10 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("billy_customer", "0002_alter_address_address_2_alter_address_address_3"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="address",
            options={"verbose_name_plural": "Addresses"},
        ),
    ]
