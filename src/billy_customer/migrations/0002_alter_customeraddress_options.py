# Generated by Django 4.0 on 2021-12-30 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billy_customer', '0001_initial_squashed_0014_customeraddress_uq_customer_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customeraddress',
            options={'ordering': ('-created',)},
        ),
    ]