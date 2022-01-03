from typing import Optional
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls.base import reverse_lazy


from shared.forms import PaginationForm, render_crispy_form
from shared.helpers.htmx import get_htmx_details
from shared.helpers.response import update_headers

from .models import Category, Product
from .forms import CategoryForm, ProductForm, ProductSearchForm


def get_search_form(request: HttpRequest, list_id: str) -> ProductSearchForm:
    search_form = ProductSearchForm(
        request.GET.copy(),
        add_url=reverse_lazy("billy_warehouse:add-product"),
        clear_url=reverse_lazy("billy_warehouse:index"),
        list_id=list_id,
    )

    if search_form.is_valid():
        return search_form
    return ProductSearchForm(
        add_url=reverse_lazy("billy_warehouse:add-product"),
        clear_url=reverse_lazy("billy_warehouse:index"),
        list_id=list_id,
    )


@login_required
def index(request: HttpRequest) -> HttpResponse:
    products_list_id = "products-list"
    search_form = get_search_form(request, list_id=products_list_id)
    pagination_form = PaginationForm(request.GET)
    products_queryset = Product.objects.visible()  # type: ignore

    if search_form.is_valid():
        products_queryset = products_queryset.filter(
            name__contains=search_form.cleaned_data["q"]
        )

    products_paginator = Paginator(products_queryset, per_page=20)
    products_page = products_paginator.get_page(pagination_form.get_page_number())

    if get_htmx_details(request):
        template_name = "billy_warehouse/products_list.html"
    else:
        template_name = "billy_warehouse/index.html"

    return render(
        request=request,
        template_name=template_name,
        context={
            "products": products_page,
            "search_form": search_form,
            "products_list_id": products_list_id,
        },
    )


@login_required
def add_product(request: HttpRequest) -> HttpResponse:
    form_id = "add-edit-product"
    product_details_id = "product-details"

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            form_id=form_id,
            product_details_id=product_details_id,
            target_url=reverse_lazy("billy_warehouse:add-product"),
            details_form_url=reverse_lazy("billy_warehouse:get-details-form-stub"),
        )

        if form.is_valid():
            details_form = form.cleaned_data["category"].details_form(request.POST)
            if details_form.is_valid():
                form.instance.details = details_form.cleaned_data
                form.save()

                return update_headers(
                    response=HttpResponse(), headers={"HX-Refresh": "true"}
                )
            else:
                response = render_crispy_form(request=request, form=details_form)
                response = update_headers(
                    response=response, headers={"HX-Retarget": f"#{product_details_id}"}
                )

                return response
        else:
            # Try to get and render an apropriate details form
            if category := form.cleaned_data.get("category"):
                details_form = category.details_form(request.POST)
                details_form.is_valid()

                rendered_details_form = render_crispy_form(
                    request=request, form=details_form
                ).content.decode()

                form.update_product_details_form(rendered_details_form)

            response = render_crispy_form(request=request, form=form)
            response = update_headers(response, {"HX-Retarget": f"#{form_id}"})

            return response
    else:
        return render_crispy_form(
            request=request,
            form=ProductForm(
                form_id=form_id,
                product_details_id=product_details_id,
                target_url=reverse_lazy("billy_warehouse:add-product"),
                details_form_url=reverse_lazy("billy_warehouse:get-details-form-stub"),
            ),
        )


@login_required
def get_details_form(request: HttpRequest) -> HttpResponse:
    category_form = CategoryForm(request.GET)

    if category_form.is_valid():
        category_instance = Category.objects.get(
            pk=category_form.cleaned_data["category"]
        )
    else:
        return HttpResponseBadRequest(category_form.errors)

    return render_crispy_form(request=request, form=category_instance.details_form)


@login_required
def edit_product(request: HttpRequest, pk_product: int) -> HttpResponse:
    form_id = "add-edit-product"
    product_details_id = "product-details"
    product = Product.objects.get(pk=pk_product)

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            form_id=form_id,
            product_details_id=product_details_id,
            target_url=reverse_lazy("billy_warehouse:edit-product", args=[product.pk]),
            details_form_url=reverse_lazy("billy_warehouse:get-details-form-stub"),
        )

        if form.is_valid():
            details_form = form.cleaned_data["category"].details_form(request.POST)
            if details_form.is_valid():
                form.instance.details = details_form.cleaned_data

                Product.objects.replace(instance=product, other=form.instance)  # type: ignore

                return update_headers(
                    response=HttpResponse(), headers={"HX-Refresh": "true"}
                )
            else:
                response = render_crispy_form(request=request, form=details_form)
                response = update_headers(
                    response=response, headers={"HX-Retarget": f"#{product_details_id}"}
                )

                return response
        else:
            # Try to get and render an apropriate details form
            if category := form.cleaned_data.get("category"):
                details_form = category.details_form(request.POST)
                details_form.is_valid()

                rendered_details_form = render_crispy_form(
                    request=request, form=details_form
                ).content.decode()

                form.update_product_details_form(rendered_details_form)

            response = render_crispy_form(request=request, form=form)
            response = update_headers(response, {"HX-Retarget": f"#{form_id}"})

            return response
    else:
        details_form = product.category.details_form(product.details)
        rendered_details_form = render_crispy_form(
            request=request, form=details_form
        ).content.decode()

        return render_crispy_form(
            request=request,
            form=ProductForm(
                instance=product,
                form_id=form_id,
                product_details_id=product_details_id,
                target_url=reverse_lazy("billy_warehouse:edit-product", args=[product.pk]),
                details_form_url=reverse_lazy("billy_warehouse:get-details-form-stub"),
                rendered_details_form=rendered_details_form,
            ),
        )
