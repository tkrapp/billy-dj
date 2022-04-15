from typing import Any

from django.urls import reverse_lazy

from billy_warehouse import models as warehouse_models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms
from django.utils.translation import gettext_lazy
from django.utils.safestring import mark_safe


from .conf import settings


class CustomerIdAndAddressForm(forms.Form):
    customer_id = forms.IntegerField()
    customer_address_id = forms.IntegerField()


class AddToCartForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=warehouse_models.Product.objects.visible()
    )
    netto_price = forms.FloatField(
        label=gettext_lazy("Netto price"),
        min_value=0,
        required=True,
        initial=1,
        widget=forms.NumberInput(attrs={"step": "0.01"}),
    )
    vat = forms.ChoiceField(
        label=gettext_lazy(
            mark_safe(gettext_lazy('<abbr title="Value Added Tax">VAT</abbr>'))
        ),
        choices=settings.VAT_CHOICES,
        initial=settings.VAT_CHOICES[0],
    )
    brutto_price = forms.FloatField(
        label=gettext_lazy("Brutto price"),
        min_value=0,
        required=True,
        initial=1,
        widget=forms.NumberInput(attrs={"step": "0.01"}),
    )
    quantity = forms.FloatField(
        label=gettext_lazy("Quantity"),
        min_value=0.1,
        widget=forms.NumberInput(attrs={"step": "0.1"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "add-to-cart-form"
        self.helper.form_action = reverse_lazy("billy_invoice:add-to-cart")

        self.helper.layout = Layout(
            Field("product"),
            Field("netto_price"),
            Field("vat"),
            Field("brutto_price"),
            Field("quantity"),
        )


class UpdateCartForm(AddToCartForm):
    product = forms.ModelChoiceField(
        queryset=warehouse_models.Product.objects.visible(),  # type: ignore
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Div(
                Field(
                    "netto_price",
                    css_class="form-control-sm",
                    # hx_get=details_form_url,
                    # hx_target=f"#{product_details_id}",
                    # hx_swap="innerHTML",
                ),
                Field(
                    "quantity",
                    css_class="form-control-sm",
                    # wrapper_class="flex-grow-1 ms-2",
                ),
                css_class="d-flex",
            )
        )
