from decimal import Decimal, getcontext
from typing import Optional

from billy_customer import models as customer_models
from billy_warehouse import models as warehouse_models
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from shared.forms import render_crispy_form

from . import forms, models
from .conf import settings
from .helpers import get_or_init_cart
from .types import CartSessionDict, VATChoices


@login_required
def index(request: HttpRequest) -> HttpResponse:
    invoices = models.Invoice.objects.all()

    return render(
        request=request,
        template_name="billy_invoice/index.html",
        context={"invoices": invoices},
    )


@login_required
def cart(request: HttpRequest) -> HttpResponse:
    customer = None
    customer_address = None
    products = None

    if cart_data := request.session.get(settings.SESSION_KEY_CART):
        print(cart_data)
        if (customer_id := cart_data["customer_id"]) is not None:
            customer = customer_models.Customer.objects.prefetch_related(
                "addresses"
            ).get(pk=customer_id)

        if (
            customer
            and (customer_address_id := cart_data["customer_address_id"]) is not None
        ):
            customer_address = customer.addresses.get(pk=customer_address_id)

        products_dict = {
            product.pk: product
            for product in warehouse_models.Product.objects.select_related(
                "category"
            ).filter(pk__in={prod["product_id"] for prod in cart_data["products"]})
        }
        products = [
            {
                **prod,
                "instance": products_dict[prod["product_id"]],
                "form": forms.UpdateCartForm(
                    {
                        "product": products_dict[prod["product_id"]],
                        "netto_price": prod["netto_price"],
                        "quantity": prod["quantity"],
                    }
                ),
            }
            for prod in cart_data["products"]
        ]
    else:
        request.session[settings.SESSION_KEY_CART] = get_or_init_cart(request)

    return render(
        request=request,
        template_name="billy_invoice/cart.html",
        context={
            "customer": customer,
            "customer_address": customer_address,
            "products": products,
        },
    )


@login_required
@require_POST
def set_customer_and_address(request: HttpRequest) -> HttpResponse:
    form = forms.CustomerIdAndAddressForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest(content=str(form.errors))

    cart_data = get_or_init_cart(request)

    cart_data["customer_id"] = form.cleaned_data["customer_id"]
    cart_data["customer_address_id"] = form.cleaned_data["customer_address_id"]
    request.session.modified = True

    return HttpResponseRedirect(redirect_to=reverse_lazy("billy_invoice:cart"))


@login_required
@require_GET
def get_add_to_cart_form(
    request: HttpRequest, product_id: Optional[int] = None
) -> HttpResponse:
    product = warehouse_models.Product.objects.get(pk=product_id)

    return render_crispy_form(
        request=request,
        form=forms.AddToCartForm(
            {
                "product": product_id,
                "netto_price": product.netto_price,
                "quantity": 1,
                "vat": VATChoices.NINETEEN,
                "brutto_price": (
                    product.netto_price * Decimal(VATChoices.NINETEEN / 100 + 1)
                ).quantize(Decimal("1.00")),
            }
        ),
    )


@login_required
@require_POST
def add_to_cart(request: HttpRequest) -> HttpResponse:
    form = forms.AddToCartForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest(content=str(form.errors))

    cart_data: Optional[CartSessionDict] = request.session.get(
        settings.SESSION_KEY_CART
    )
    if cart_data is None:
        cart_data = get_or_init_cart(request)
        request.session[settings.SESSION_KEY_CART] = cart_data

    if product := [
        prod
        for prod in cart_data["products"]
        if prod["product_id"] == form.cleaned_data["product"].pk
    ]:
        product[0]["netto_price"] = form.cleaned_data["netto_price"]
        product[0]["quantity"] += form.cleaned_data["quantity"]
    else:
        cart_data["products"].append(
            {
                "product_id": form.cleaned_data["product"].pk,
                "netto_price": form.cleaned_data["netto_price"],
                "quantity": form.cleaned_data["quantity"],
            }
        )

    request.session.modified = True

    return HttpResponseRedirect(redirect_to=reverse_lazy("billy_invoice:cart"))
