from django.urls import path

from . import apps, views

app_name = apps.BillyInvoiceConfig.name
urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.cart, name="cart"),
    path(
        "set-customer-and-address",
        views.set_customer_and_address,
        name="set-customer-and-address",
    ),
    path("add-to-cart", views.add_to_cart, name="add-to-cart"),
    path(
        "add-to-cart-form/<int:product_id>",
        views.get_add_to_cart_form,
        name="add-to-cart-form",
    ),
]
