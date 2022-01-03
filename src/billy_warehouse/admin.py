from decimal import Decimal
from typing import Optional

from django.contrib import admin
from django.db import models as django_models
from django.utils.translation import gettext_lazy

from shared.admin import PrettyJSONWidget

from . import models


@admin.register(models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = ["created", "modified"]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "vendor",
        "netto_price",
        "details",
        "hidden",
    ]
    readonly_fields = ["created", "modified"]


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity"]
    readonly_fields = ["created", "modified"]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = ["created", "modified"]
    formfield_overrides = {django_models.JSONField: {"widget": PrettyJSONWidget}}
