from django.urls import path

from . import apps, views

app_name = apps.BillyWarehouseConfig.name
urlpatterns = [
    path("", views.index, name="index"),
]
