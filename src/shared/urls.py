from django.urls import path

from . import apps, views

app_name = apps.SharedConfig.name
urlpatterns = [
    path("search-postal-code", views.search_postal_code, name="search-postal-code"),
]
