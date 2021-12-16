# Generated by Django 4.0 on 2021-12-14 22:32

from django.db import migrations, models


def make_addresses_unique(apps, schema_editor):
    """
    Uniquify addresses and update corresponding tables.
    """
    db_alias = schema_editor.connection.alias
    CustomerAddress = apps.get_model("billy_customer", "CustomerAddress")

    seen = set()
    key_getter = lambda obj: (obj.customer_id, obj.address_id)

    for customer_address_rel in CustomerAddress.objects.using(db_alias).all():
        key = key_getter(customer_address_rel)

        if key not in seen:
            seen.add(key)
        else:
            customer_address_rel.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("billy_customer", "0013_address_uq_everything"),
    ]

    operations = [
        migrations.RunPython(
            code=make_addresses_unique, reverse_code=migrations.RunPython.noop
        ),
        migrations.AddConstraint(
            model_name="customeraddress",
            constraint=models.UniqueConstraint(
                fields=("customer", "address"), name="uq_customer_address"
            ),
        ),
    ]