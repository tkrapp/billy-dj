from typing import cast
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from shared.forms import render_crispy_form
from django.db import transaction
from django.db.models import Q
from django_htmx.middleware import HtmxDetails
from itertools import groupby

from shared.helpers.htmx import get_htmx_details

from .forms import AddressForm, CustomerForm, SearchForm
from .models import Address, Customer

NAMESPACE = "billy_customer"


def get_search_form(request: HttpRequest) -> SearchForm:
    search_form = SearchForm(
        request.GET.copy(), add_url=reverse_lazy("billy_customer:add-customer")
    )

    if search_form.is_valid():
        return search_form
    return SearchForm(add_url=reverse_lazy("billy_customer:add-customer"))


def get_first_letter_of_last_name(obj: Customer) -> str:
    return obj.last_name[0].upper()


@login_required
def index(request: HttpRequest) -> HttpResponse:
    customers = Customer.objects.visible()  # type: ignore
    search_form = get_search_form(request)

    if search_form.is_valid():
        words = search_form.cleaned_data["q"].split()

        for word in words:
            customers = customers.filter(
                Q(first_name__contains=word) | Q(last_name__contains=word)
            )

    return render(
        request=request,
        template_name=f"{NAMESPACE}/index.html",
        context={
            "search_form": search_form,
            "grouped_customers": [
                (key, list(group))
                for key, group in groupby(
                    customers.order_by("last_name", "first_name"),
                    key=get_first_letter_of_last_name,
                )
            ],
        },
    )


@login_required
def details(request: HttpRequest, pk: int) -> HttpResponse:
    customer = Customer.objects.get(pk=pk)
    search_form = get_search_form(request)

    return render(
        request=request,
        template_name=f"{NAMESPACE}/details.html",
        context={
            "customer": customer,
            "search_form": search_form,
            "customer_addresses": customer.addresses.order_by("customeraddress"),
        },
    )


@login_required
def edit_customer_data(request: HttpRequest, pk: int) -> HttpResponse:
    customer = Customer.objects.get(pk=pk)
    target_url = reverse_lazy(
        "billy_customer:edit-customer-data", kwargs={"pk": customer.pk}
    )
    edit_form = CustomerForm(instance=customer, target_url=target_url)

    if request.method == "POST":
        edit_form = CustomerForm(request.POST, target_url=target_url)

        if edit_form.is_valid():
            customer = customer.change_data(**edit_form.cleaned_data)
            edit_form = CustomerForm(instance=customer, target_url=target_url)

            response = render_crispy_form(request, edit_form)
            response.headers["HX-Redirect"] = customer.get_absolute_url()
            return response
        else:
            return render_crispy_form(request, edit_form)

    return render_crispy_form(request=request, form=edit_form)


@login_required
def edit_address(request: HttpRequest, pk: int, address_pk: int) -> HttpResponse:
    customer = Customer.objects.get(pk=pk)
    address = Address.objects.get(pk=address_pk)

    if not address in customer.addresses:
        raise Exception("NOO")

    address_form = AddressForm(instance=address, target_url="...")

    return render(
        request=request,
        template_name=f"{NAMESPACE}/add_edit_address.html",
        context={"form": address_form},
    )


@login_required
def add_address(request: HttpRequest, pk: int) -> HttpResponse:
    form_id = "add-edit-address"
    if request.method == "POST":
        customer = Customer.objects.get(pk=pk)
        address_form = AddressForm(
            request.POST,
            target_url=request.path,
            target="#address-list",
            form_id=form_id,
        )
        headers = {}
        htmx_details = get_htmx_details(request)
        saved = False
        status = None

        with transaction.atomic():
            if address_form.is_valid():
                address_form.save()
                customer.addresses.add(address_form.instance)
                saved = True
            elif address := address_form.get_already_existing():
                customer.addresses.add(address)
                saved = True
            elif not address_form.is_valid() and htmx_details is not None:
                headers["HX-Retarget"] = f"#{form_id}"

        if saved:
            return render(
                request=request,
                template_name="billy_customer/details_customer_addresses.html",
                context={
                    "customer_addresses": customer.addresses.all().order_by(
                        "customeraddress"
                    )
                },
            )

        response = render_crispy_form(request, address_form)
        for header, value in headers.items():
            response.headers[header] = value

        if status:
            response.status_code = status

        return response
    else:
        return render_crispy_form(
            request, AddressForm(target_url=request.path, target="#address-list")
        )


@login_required
def add_customer(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        customer_form = CustomerForm(request.POST, target_url=request.path)

        if customer_form.is_valid():
            customer_form.save()

            response = HttpResponse(
                "",
                status=201,
                headers={
                    "HX-Redirect": reverse_lazy(
                        "billy_customer:details",
                        kwargs={"pk": customer_form.instance.pk},
                    ),
                },
            )
            return response

        return render_crispy_form(request=request, form=customer_form)

    return render_crispy_form(
        request=request, form=CustomerForm(target_url=request.path)
    )
