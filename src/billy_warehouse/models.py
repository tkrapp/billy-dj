from decimal import Decimal
from typing import Optional
from django.db import models
from django.utils.translation import gettext, gettext_lazy

from model_utils.models import TimeStampedModel


class Vendor(TimeStampedModel):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"), max_length=100, unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Vendor")
        verbose_name_plural = gettext_lazy("Vendors")


class Category(TimeStampedModel):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"), max_length=100, unique=True
    )

    def __str__(self) -> str:
        return gettext(self.name)

    class Meta:
        verbose_name = gettext_lazy("Category")
        verbose_name_plural = gettext_lazy("Categories")


class Product(TimeStampedModel):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"), max_length=255, unique=True
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name=gettext_lazy("Category"),
        on_delete=models.RESTRICT,
    )
    vendor = models.ForeignKey(
        to=Vendor, verbose_name=gettext_lazy("Vendor"), on_delete=models.RESTRICT
    )
    netto_price = models.PositiveBigIntegerField(
        verbose_name=gettext_lazy("Netto price (in Cents)")
    )
    details = models.JSONField(verbose_name=gettext_lazy("Details"))

    def __str__(self) -> str:
        return f"({self.vendor.name}) {self.name}"

    @property
    def netto_price_in_euro(self) -> Optional[Decimal]:
        if not self.netto_price:
            return None
        return (Decimal(self.netto_price) / Decimal(100)).quantize(Decimal("1.00"))

    class Meta:
        verbose_name = gettext_lazy("Product")
        verbose_name_plural = gettext_lazy("Products")


class Stock(TimeStampedModel):
    product = models.ForeignKey(
        to=Product, verbose_name=gettext_lazy("Product"), on_delete=models.RESTRICT
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=gettext_lazy("Quantity"))

    class Meta:
        verbose_name = gettext_lazy("Stock")
        verbose_name_plural = gettext_lazy("Stocks")
