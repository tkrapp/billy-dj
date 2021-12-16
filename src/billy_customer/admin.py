from django.contrib import admin

from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["full_name"]
    readonly_fields = ["created", "modified"]
    search_fields = ["fist_name", "last_name", "id"]


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["postal_code", "city", "address_1", "address_2", "address_3"]
    readonly_fields = ["created", "modified"]


@admin.register(models.CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ["customer", "address"]
    search_fields = ["customer__name"]
