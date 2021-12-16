from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from . import models


@login_required
def index(request: HttpRequest) -> HttpResponse:
    invoices = models.Invoice.objects.all()

    return render(
        request=request,
        template_name="billy_invoice/index.html",
        context={"invoices": invoices},
    )
