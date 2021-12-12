from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy
from decimal import Decimal
from django.utils import timezone

import billy_warehouse.models
import billy_customer.models
from model_utils.models import TimeStampedModel


def today() -> date:
    return timezone.now().date()


class Invoice(TimeStampedModel, models.Model):
    invoice_number = models.CharField(
        verbose_name=gettext_lazy("Invoice number"), max_length=20
    )
    invoice_date = models.DateField(
        verbose_name=gettext_lazy("Invoice date"), default=today
    )
    customer = models.ForeignKey(
        to=billy_customer.models.Customer,
        verbose_name=gettext_lazy("Customer"),
        on_delete=models.RESTRICT,
    )
    address = models.ForeignKey(
        to=billy_customer.models.Address,
        verbose_name=gettext_lazy("Address"),
        on_delete=models.RESTRICT,
    )

    class Meta:
        verbose_name = gettext_lazy("Invoice")
        verbose_name_plural = gettext_lazy("Invoices")


class InvoiceItem(TimeStampedModel, models.Model):
    class VATChoices(models.IntegerChoices):
        NINETEEN = 19
        SEVEN = 7

    invoice = models.ForeignKey(
        to=Invoice, verbose_name=gettext_lazy("Invoice"), on_delete=models.RESTRICT
    )
    product = models.ForeignKey(
        to=billy_warehouse.models.Product,
        verbose_name=gettext_lazy("Product"),
        on_delete=models.RESTRICT,
    )
    quantity = models.PositiveBigIntegerField(verbose_name=gettext_lazy("Quantity"))
    netto_price_per_unit = models.PositiveBigIntegerField(
        verbose_name=gettext_lazy("Netto price per unit (in Cents)")
    )
    vat_rate = models.PositiveSmallIntegerField(
        verbose_name=gettext_lazy("VAT rate"), choices=VATChoices.choices
    )

    @property
    def netto_price_in_euro(self) -> Decimal:
        return (Decimal(self.netto_price_per_unit) / Decimal(100)).quantize(
            Decimal("1.00")
        )

    @netto_price_in_euro.setter
    def netto_price_in_euro(self, value: Decimal):
        self.netto_price_per_unit = int((value * 100).quantize(Decimal("1")))

    class Meta:
        verbose_name = gettext_lazy("Invoice item")
        verbose_name_plural = gettext_lazy("Invoice items")
