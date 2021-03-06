"""billy_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.urls.base import reverse
from django.urls.conf import include
from django.utils.translation import gettext_lazy
from django.contrib.auth import urls

admin.site.site_header = gettext_lazy("Billy Administration")
admin.site.site_title = gettext_lazy("Billy Administration Portal")
admin.site.index_title = gettext_lazy("Welcome to Billy's Administration Portal")


def redirect_to_start(request: HttpRequest) -> HttpResponse:
    return redirect(to=reverse(viewname="start:index"))


urlpatterns = [
    path("", redirect_to_start),
    path("start/", include("start.urls")),
    path("customers/", include("billy_customer.urls")),
    path("warehouse/", include("billy_warehouse.urls")),
    path("invoices/", include("billy_invoice.urls")),
    path("shared/", include("shared.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
