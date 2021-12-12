from django.contrib import admin

from . import models


class InvoiceItemInline(admin.TabularInline):
    model = models.InvoiceItem


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "created", "modified", "customer"]
    inlines = [
        InvoiceItemInline,
    ]
    readonly_fields = ["created", "modified"]
