from django.urls import path

from . import apps, views

app_name = apps.BillyCustomerConfig.name
urlpatterns = [
    path("", views.index, name="index"),
    path("details/<int:pk>", views.details, name="details"),
]
