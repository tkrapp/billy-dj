from typing import Any, Type
from django.db.models.signals import post_save

from . import models


def update_product_search(
    sender: Type[models.Product], instance: models.Product, **kwargs: Any
):
    print(f"Updated {instance.pk}")
    models.ProductSearch.objects.update_or_create(
        product=instance, defaults={"search_document": instance.search_document}
    )


post_save.connect(update_product_search, sender=models.Product)
