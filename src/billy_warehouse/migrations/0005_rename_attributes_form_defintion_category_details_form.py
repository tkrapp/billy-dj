# Generated by Django 4.0 on 2021-12-31 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billy_warehouse', '0004_alter_category_attributes_form_defintion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='attributes_form_defintion',
            new_name='details_form',
        ),
    ]
