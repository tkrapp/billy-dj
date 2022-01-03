from decimal import Decimal
from typing import Optional
from crispy_forms.helper import FormHelper

from django import forms
from django.db import models
from django.utils.translation import gettext, gettext_lazy
from model_utils.models import TimeStampedModel
from shared.models import HideableManager, HideableModel, JSONFormDefinitionField
from django.core.exceptions import ValidationError


class DefaultDetailsForm(forms.Form):
    description = forms.CharField(
        label=gettext_lazy("Description"), widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class Vendor(TimeStampedModel):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"), max_length=100, unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Vendor")
        verbose_name_plural = gettext_lazy("Vendors")
        ordering = ["name"]


class Category(TimeStampedModel):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"), max_length=100, unique=True
    )
    details_form = JSONFormDefinitionField(
        verbose_name=gettext_lazy("Attributes form definition"),
        null=True,
        blank=True,
        default_form_class=DefaultDetailsForm,
    )

    def __str__(self) -> str:
        return gettext(self.name)

    class Meta:
        verbose_name = gettext_lazy("Category")
        verbose_name_plural = gettext_lazy("Categories")
        ordering = ["name"]


class Product(HideableModel, TimeStampedModel):
    name = models.CharField(verbose_name=gettext_lazy("Name"), max_length=255)
    category = models.ForeignKey(
        to=Category,
        verbose_name=gettext_lazy("Category"),
        on_delete=models.RESTRICT,
    )
    vendor = models.ForeignKey(
        to=Vendor, verbose_name=gettext_lazy("Vendor"), on_delete=models.RESTRICT
    )
    netto_price = models.DecimalField(
        verbose_name=gettext_lazy("Netto price (in Euro)"),
        max_digits=20,
        decimal_places=2,
    )
    details = models.JSONField(verbose_name=gettext_lazy("Details"))

    objects = HideableManager()

    def __str__(self) -> str:
        return f"({self.vendor.name}) {self.name}"

    class Meta:
        verbose_name = gettext_lazy("Product")
        verbose_name_plural = gettext_lazy("Products")
        ordering = ["name", "category__name", "vendor__name"]


class Stock(TimeStampedModel):
    product = models.ForeignKey(
        to=Product, verbose_name=gettext_lazy("Product"), on_delete=models.RESTRICT
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=gettext_lazy("Quantity"))

    class Meta:
        verbose_name = gettext_lazy("Stock")
        verbose_name_plural = gettext_lazy("Stocks")
