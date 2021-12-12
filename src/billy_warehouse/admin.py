from decimal import Decimal
from typing import Optional
from django.contrib import admin
from django.utils.translation import gettext_lazy

from . import models


@admin.register(models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = ["created", "modified"]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "vendor", "netto_price_in_euro", "details"]
    readonly_fields = ["created", "modified", "netto_price_in_euro"]

    @admin.display(description=gettext_lazy("Price in EUR"))
    def netto_price_in_euro(self, obj: models.Product) -> Optional[Decimal]:
        return obj.netto_price_in_euro


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity"]
    readonly_fields = ["created", "modified"]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = ["created", "modified"]
