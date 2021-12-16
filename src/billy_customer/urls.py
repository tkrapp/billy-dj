from django.urls import path

from . import apps, views

app_name = apps.BillyCustomerConfig.name
urlpatterns = [
    path("", views.index, name="index"),
    path("add-customer", views.add_customer, name="add-customer"),
    path("details/<int:pk>", views.details, name="details"),
    path(
        "details/<int:pk>/edit-customer-data",
        views.edit_customer_data,
        name="edit-customer-data",
    ),
    path(
        "details/<int:pk>/edit-address/<int:address_pk>",
        views.edit_address,
        name="edit-address",
    ),
    path(
        "details/<int:pk>/add-address",
        views.add_address,
        name="add-address",
    ),
]
