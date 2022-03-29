from typing import Optional

from crispy_forms.bootstrap import StrictButton, FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Row, HTML
from django import forms
from django.core.exceptions import ValidationError
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy
from shared.forms import SearchInput
from shared.helpers.bs_icons import bsicon

from .models import Address, Customer


class SearchForm(forms.Form):
    q = forms.CharField(
        label=gettext_lazy("Search text"), widget=SearchInput(attrs={"id": "id_q"})
    )

    def __init__(
        self, *args, add_url: str, clear_url: str, list_id: Optional[str], **kwargs
    ):
        super().__init__(*args, **kwargs)

        clear_button_params = {}
        if list_id is not None:
            clear_button_params["hx_target"] = f"#{list_id}"

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = "GET"
        self.helper.form_action = reverse("billy_customer:index")
        self.helper.layout = Layout(
            Div(
                FieldWithButtons(
                    Field(
                        "q",
                        placeholder=gettext_lazy("Customer name"),
                        css_class="form-control-sm",
                    ),
                    HTML(f"""
                        <a
                            class="btn btn-secondary btn-sm"
                            href="{clear_url}"
                            aria_label={gettext_lazy("Clear search")}
                        >
                            {bsicon("x-lg")}
                        </a>
                        """,
                    ),
                    StrictButton(
                        mark_safe(bsicon("search")),
                        css_class="btn btn-primary btn-sm",
                        type="submit",
                        aria_label=gettext_lazy("Search"),
                        title=gettext_lazy("Search"),
                    ),
                    css_class="me-2 flex-fill",
                ),
                ButtonHolder(
                    StrictButton(
                        mark_safe(bsicon("plus-lg")),
                        css_class="btn btn-success btn-sm",
                        aria_label=gettext_lazy("Add"),
                        title=gettext_lazy("Add new customer"),
                        **{
                            "hx-get": add_url,
                            "hx-target": "#add-edit-user-modal-content",
                            "hx-trigger": "click",
                        },
                    ),
                ),
                css_class="d-flex justify-content-evenly",
            ),
        )


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, target_url: str, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "edit-customer-data"

        self.helper.attrs = {
            "hx-post": target_url,
            "hx-target": "this",
            "hx-swap": "outerHTML",
        }

    class Meta:
        model = Customer
        fields = ["first_name", "last_name"]


class AddressForm(forms.ModelForm):
    def __init__(
        self,
        *args,
        target_url: Optional[str] = None,
        target: str = "this",
        form_id: str = "add-edit-address",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = form_id
        self.helper.layout = Layout(
            Row(
                Field(
                    "address_1",
                    css_class="form-control-sm",
                    wrapper_class="col col-12",
                ),
            ),
            Row(
                Field(
                    "address_2",
                    css_class="form-control-sm",
                    wrapper_class="col col-12",
                ),
            ),
            Row(
                Field(
                    "address_3",
                    css_class="form-control-sm",
                    wrapper_class="col col-12",
                ),
            ),
            Row(
                Field(
                    "postal_code",
                    css_class="form-control-sm",
                    wrapper_class="col col-sm-4",
                    autocomplete="off",
                ),
                Field(
                    "city",
                    css_class="form-control-sm",
                    wrapper_class="col col-sm-8",
                ),
                css_class="flex-d",
            ),
        )

        if target_url:
            self.helper.attrs = {
                "hx-post": target_url,
                "hx-target": target,
                "hx-swap": "outerHTML",
            }

    def get_already_existing(self) -> Optional[Address]:
        try:
            return Address.objects.get(**{key: self.data[key] for key in self.fields})
        except Address.DoesNotExist:
            return None

    def clean_postal_code(self):
        errors = []
        postal_code: str = self.cleaned_data["postal_code"]

        if len(postal_code) < 5:
            errors.append(
                ValidationError(
                    gettext_lazy("Postal code must have a length of five characters")
                )
            )

        if not postal_code.isdecimal():
            errors.append(
                ValidationError(
                    gettext_lazy("Postal code must contain only decimal digits")
                )
            )

        if errors:
            raise ValidationError(errors)

        return postal_code

    class Meta:
        model = Address
        exclude = ["hidden"]
