import urllib.parse
from itertools import groupby
from typing import Optional, cast

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_http_methods
from shared.forms import PaginationForm, render_crispy_form
from shared.helpers.htmx import get_htmx_details

from .conf import settings
from .forms import AddressForm, CustomerForm, SearchForm
from .models import Address, Customer, CustomerAddress

NAMESPACE = "billy_customer"


def get_search_form(request: HttpRequest, list_id: Optional[str] = None) -> SearchForm:
    search_form = SearchForm(
        request.GET.copy(),
        add_url=reverse_lazy("billy_customer:add-customer"),
        clear_url=reverse_lazy("billy_customer:index"),
        list_id=list_id,
    )

    if search_form.is_valid():
        return search_form
    return SearchForm(
        add_url=reverse_lazy("billy_customer:add-customer"),
        clear_url=reverse_lazy("billy_customer:index"),
        list_id=list_id,
    )


def get_first_letter_of_last_name(obj: Customer) -> str:
    return obj.last_name[0].upper()


@login_required
def index(request: HttpRequest) -> HttpResponse:
    customers_list_id = "customers-list"
    customers_queryset = Customer.objects.visible()  # type: ignore
    search_form = get_search_form(request, customers_list_id)
    pagination_form = PaginationForm(request.GET)
    search_form_qs = ""

    if search_form.is_valid():
        words = search_form.cleaned_data["q"].split()

        for word in words:
            customers_queryset = customers_queryset.filter(
                Q(first_name__contains=word) | Q(last_name__contains=word)
            )

        search_form_qs = f"?{urllib.parse.urlencode(search_form.cleaned_data)}"

    if get_htmx_details(request):
        template_name = f"{NAMESPACE}/customers_list.html"
    else:
        template_name = f"{NAMESPACE}/index.html"

    customers_paginator = Paginator(
        customers_queryset.order_by("last_name", "first_name"),
        per_page=settings.INDEX_PAGE_SIZE,
    )
    customers_page = customers_paginator.get_page(pagination_form.get_page_number())

    response = render(
        request=request,
        template_name=template_name,
        context={
            "search_form": search_form,
            "search_form_qs": search_form_qs,
            "grouped_customers": [
                (key, list(group))
                for key, group in groupby(
                    customers_page,
                    key=get_first_letter_of_last_name,
                )
            ],
            "customers": customers_page,
            "customers_list_id": customers_list_id,
        },
    )

    return response


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
            "customer_addresses": customer.get_visible_addresses(),
        },
    )


@login_required
def edit_customer_data(request: HttpRequest, pk: int) -> HttpResponse:
    customer: Customer = Customer.objects.get(pk=pk)
    target_url = reverse_lazy(
        "billy_customer:edit-customer-data", kwargs={"pk": customer.pk}
    )
    edit_form = CustomerForm(instance=customer, target_url=target_url)

    if request.method == "POST":
        edit_form = CustomerForm(request.POST, target_url=target_url)

        if edit_form.is_valid():
            customer = customer.update(edit_form.cleaned_data)
            edit_form = CustomerForm(instance=customer, target_url=target_url)

            response = render_crispy_form(request, edit_form)
            response.headers["HX-Redirect"] = customer.get_absolute_url()
            return response
        else:
            return render_crispy_form(request, edit_form)

    return render_crispy_form(request=request, form=edit_form)


@login_required
def edit_address(request: HttpRequest, pk: int, address_pk: int) -> HttpResponse:
    form_id = "add-edit-address"
    customer = Customer.objects.get(pk=pk)

    try:
        address: Address = customer.addresses.get(pk=address_pk)
    except Address.DoesNotExist:
        raise Http404(gettext_lazy("Could not find a matching address"))

    if request.method == "POST":
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
        new_address = None

        with transaction.atomic():
            if address_form.is_valid():
                address_form.save()
                new_address = address_form.instance
                saved = True
            elif existing_address := address_form.get_already_existing():
                new_address = existing_address
                saved = True
            elif not address_form.is_valid() and htmx_details is not None:
                headers["HX-Retarget"] = f"#{form_id}"

            if saved:
                query = CustomerAddress.objects.filter(
                    customer=customer, address=new_address
                )
                if query.count():
                    query.update(hidden=False)
                else:
                    CustomerAddress.objects.get(
                        customer=customer, address=address
                    ).update({"customer": customer, "address": new_address})

                return render(
                    request=request,
                    template_name="billy_customer/details_customer_addresses.html",
                    context={
                        "customer": customer,
                        "customer_addresses": customer.get_visible_addresses(),
                    },
                )

        response = render_crispy_form(request, address_form)
        for header, value in headers.items():
            response.headers[header] = value

        if status:
            response.status_code = status

        return response

    address_form = AddressForm(
        instance=address,
        target_url=reverse_lazy(
            "billy_customer:edit-address", args=(customer.pk, address.pk)
        ),
        target="#address-list",
    )

    return render_crispy_form(request=request, form=address_form)


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
        new_address = None

        with transaction.atomic():
            if address_form.is_valid():
                address_form.save()
                new_address = address_form.instance
                saved = True
            elif address := address_form.get_already_existing():
                new_address = address
                saved = True
            elif not address_form.is_valid() and htmx_details is not None:
                headers["HX-Retarget"] = f"#{form_id}"

            if saved:
                query = CustomerAddress.objects.filter(
                    customer=customer, address=new_address
                )
                if query.count():
                    query.update(hidden=False)
                else:
                    customer.addresses.add(new_address)

                return render(
                    request=request,
                    template_name="billy_customer/details_customer_addresses.html",
                    context={
                        "customer": customer,
                        "customer_addresses": customer.get_visible_addresses(),
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


@login_required
@require_http_methods(["DELETE"])
def remove_address(request: HttpRequest, pk: int, address_pk: int) -> HttpResponse:
    customer = Customer.objects.get(pk=pk)
    customer_address_relation = CustomerAddress.objects.get(
        customer=customer, address_id=address_pk
    )
    customer_address_relation.hide()

    return render(
        request=request,
        template_name="billy_customer/details_customer_addresses.html",
        context={
            "customer": customer,
            "customer_addresses": customer.get_visible_addresses(),
        },
    )
