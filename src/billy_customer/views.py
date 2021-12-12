from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import SearchForm
from .models import Customer

NAMESPACE = "billy_customer"


def get_search_form(request: HttpRequest) -> SearchForm:
    search_form = SearchForm(request.GET.copy())

    if search_form.is_valid():
        return search_form
    return SearchForm()


def index(request: HttpRequest) -> HttpResponse:
    customers = Customer.objects.all()
    search_form = get_search_form(request)

    if search_form.is_valid():
        customers = customers.filter(name__contains=search_form.cleaned_data["q"])

    return render(
        request=request,
        template_name=f"{NAMESPACE}/index.html",
        context={"search_form": search_form, "customers": customers},
    )


def details(request: HttpRequest, pk: int) -> HttpResponse:
    customer = Customer.objects.get(pk=pk)
    search_form = get_search_form(request)

    return render(
        request=request,
        template_name=f"{NAMESPACE}/details.html",
        context={"customer": customer, "search_form": search_form},
    )
