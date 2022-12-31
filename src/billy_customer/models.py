from __future__ import annotations
from datetime import datetime

from typing import Any, Mapping
from typing_extensions import Self
from django.db import models, transaction
from django.urls.base import reverse
from django.utils.translation import gettext_lazy

from model_utils.models import TimeStampedModel

from shared.models import HideableModel, HideableManager


class Address(HideableModel, TimeStampedModel):
    address_1 = models.CharField(verbose_name=gettext_lazy("Address 1"), max_length=100)
    address_2 = models.CharField(
        verbose_name=gettext_lazy("Address 2"), max_length=100, blank=True
    )
    address_3 = models.CharField(
        verbose_name=gettext_lazy("Address 3"), max_length=100, blank=True
    )
    city = models.CharField(verbose_name=gettext_lazy("City"), max_length=100)
    postal_code = models.CharField(
        verbose_name=gettext_lazy("Postal code"), max_length=5
    )

    objects = HideableManager()

    def __str__(self) -> str:
        street = ",".join(
            field for field in [self.address_1, self.address_2, self.address_3] if field
        )
        return f"{street}, {self.postal_code} {self.city}"

    class Meta:
        verbose_name = gettext_lazy("Address")
        verbose_name_plural = gettext_lazy("Addresses")
        constraints = [
            models.UniqueConstraint(
                name="uq_everything",
                fields=["address_1", "address_2", "address_3", "city", "postal_code"],
            )
        ]


class Customer(HideableModel, TimeStampedModel):
    number = models.PositiveIntegerField(
        verbose_name=gettext_lazy("Customer number"), null=True
    )
    first_name = models.CharField(
        verbose_name=gettext_lazy("First name"), max_length=100
    )
    last_name = models.CharField(verbose_name=gettext_lazy("Last name"), max_length=100)
    addresses = models.ManyToManyField(
        to=Address, verbose_name=gettext_lazy("Address"), through="CustomerAddress"
    )

    objects = HideableManager()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self):
        return reverse("billy_customer:details", args=(self.pk,))

    def update(self, data: Mapping[str, Any]) -> Customer:
        with transaction.atomic():
            clone = super().update(data)

            for customer_address_relation in CustomerAddress.objects.visible().filter(
                customer=self
            ):
                new_relation = customer_address_relation.clone()
                new_relation.customer = clone
                new_relation.save()

            return clone

    def get_visible_addresses(self) -> list[tuple[Address, datetime]]:
        return [
            (customer_address.address, customer_address.modified)
            for customer_address in CustomerAddress.objects.visible()
            .filter(customer=self)
            .select_related("address")
            .order_by("address")
        ]

    class Meta:
        verbose_name = gettext_lazy("Customer")
        verbose_name_plural = gettext_lazy("Customers")


class CustomerAddress(HideableModel, TimeStampedModel):
    customer = models.ForeignKey(
        to=Customer, verbose_name=gettext_lazy("Customer"), on_delete=models.RESTRICT
    )
    address = models.ForeignKey(
        to=Address, verbose_name=gettext_lazy("Address"), on_delete=models.RESTRICT
    )

    objects: HideableManager = HideableManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="uq_customer_address",
                fields=["customer", "address"],
            )
        ]
        ordering = ("-created",)
