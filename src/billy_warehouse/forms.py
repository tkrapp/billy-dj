from typing import Any, Mapping, Optional
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, HTML
from django import forms
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy
from shared.forms import SearchInput

from shared.helpers.bs_icons import bsicon

from .models import Product


class ProductForm(forms.ModelForm):
    # netto_price = forms.FloatField(
    #     label=gettext_lazy("Netto price in EUR"), min_value=0
    # )

    def __init__(
        self,
        data: Optional[Mapping[str, Any]] = None,
        *args: Any,
        form_id: str,
        product_details_id: str,
        target_url: str,
        details_form_url: str,
        rendered_details_form: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(data, *args, **kwargs)
        product_details_params = []

        if rendered_details_form:
            product_details_params.append(HTML(rendered_details_form))

        self.helper = FormHelper()
        self.helper.attrs = {
            "hx-post": target_url,
            "hx-target": "this",
            "hx-swap": "outerHTML",
        }
        self.helper.form_id = form_id
        self.helper.layout = Layout(
            Div(
                Field(
                    "category",
                    css_class="form-control-sm",
                    hx_get=details_form_url,
                    hx_target=f"#{product_details_id}",
                    hx_swap="innerHTML",
                ),
                Field(
                    "vendor",
                    css_class="form-control-sm",
                    wrapper_class="flex-grow-1 ms-2",
                ),
                css_class="d-flex",
            ),
            Div(
                Field("name", css_class="form-control-sm"),
                Field("netto_price", css_class="form-control-sm"),
            ),
            Div(*product_details_params, css_id=product_details_id),
        )

    def update_product_details_form(self, raw_html: str):
        """Add a rendered details form to the current form"""
        self.helper.layout.fields[2].fields.append(HTML(raw_html))  # type: ignore

    class Meta:
        model = Product
        fields = ["category", "vendor", "name", "netto_price"]


class ProductSearchForm(forms.Form):
    q = forms.CharField(
        label=gettext_lazy("Search text"), widget=SearchInput(attrs={"id": "id_q"})
    )

    def __init__(self, *args, add_url: str, clear_url: str, list_id: str, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = "GET"
        self.helper.form_action = reverse_lazy("billy_warehouse:index")
        self.helper.layout = Layout(
            Div(
                FieldWithButtons(
                    Field(
                        "q",
                        placeholder=gettext_lazy("Product name"),
                        css_class="form-control-sm",
                    ),
                    StrictButton(
                        mark_safe(bsicon("x-lg")),
                        css_class="btn btn-secondary btn-sm",
                        type="button",
                        aria_label=gettext_lazy("Clear search"),
                        title=gettext_lazy("Clear search"),
                        hx_get=clear_url,
                        hx_target=f"#{list_id}",
                        hx_push_url="true",
                        hx_swap="outerHTML",
                        data_script=f"""
                            on click put "" into
                            #{self.fields["q"].widget.attrs["id"]}.value
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
                        title=gettext_lazy("Add new product"),
                        **{
                            "hx-get": add_url,
                            "hx-target": "#add-edit-product-modal-content",
                            "hx-trigger": "click",
                        },
                    ),
                ),
                css_class="d-flex justify-content-evenly",
            ),
        )


class CategoryForm(forms.Form):
    category = forms.IntegerField(label=gettext_lazy("Category"), min_value=1)
