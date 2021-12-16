# Generated by Django 4.0 on 2021-12-14 22:19

from itertools import groupby
from operator import attrgetter

from django.db import migrations, models


def make_addresses_unique(apps, schema_editor):
    """
    Uniquify addresses and update corresponding tables.
    """
    db_alias = schema_editor.connection.alias
    Address = apps.get_model("billy_customer", "Address")
    CustomerAddress = apps.get_model("billy_customer", "CustomerAddress")
    Invoice = apps.get_model("billy_invoice", "Invoice")

    seen = {}
    key_getter = attrgetter(
        "address_1", "address_2", "address_3", "city", "postal_code"
    )

    for address in Address.objects.using(db_alias).all():
        key = key_getter(address)

        if key not in seen:
            seen[key] = address.pk
        else:
            new_pk = seen[key]
            CustomerAddress.objects.using(db_alias).filter(
                address_id=address.pk
            ).update(address_id=new_pk)
            Invoice.objects.using(db_alias).filter(address_id=address.pk).update(
                address_id=new_pk
            )
            address.delete()


class Migration(migrations.Migration):

    dependencies = [
        (
            "billy_customer",
            "0012_remove_customer_name_alter_customer_first_name_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            code=make_addresses_unique, reverse_code=migrations.RunPython.noop
        ),
        migrations.AddConstraint(
            model_name="address",
            constraint=models.UniqueConstraint(
                fields=("address_1", "address_2", "address_3", "city", "postal_code"),
                name="uq_everything",
            ),
        ),
    ]