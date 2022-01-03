from django.urls import path

from . import apps, views

app_name = apps.BillyWarehouseConfig.name
urlpatterns = [
    path("", views.index, name="index"),
    path("add-product", views.add_product, name="add-product"),
    path("edit-product/<int:pk_product>", views.edit_product, name="edit-product"),
    path("get-details-form", views.get_details_form, name="get-details-form-stub"),
    path(
        "get-details-form/<int:pk_category>",
        views.get_details_form,
        name="get-details-form",
    ),
]
