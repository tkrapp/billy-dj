from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit
from django import forms
from django.urls.base import reverse
from django.utils.translation import gettext_lazy


class SearchForm(forms.Form):
    q = forms.CharField(label=gettext_lazy("Search text"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = "GET"
        self.helper.form_action = reverse("billy_customer:index")
        self.helper.layout = Layout(
            Div(
                Field(
                    "q",
                    placeholder="Hans Müller",
                    css_class="form-control-sm",
                    wrapper_class="flex-fill me-2",
                ),
                ButtonHolder(
                    Submit(
                        "submit",
                        gettext_lazy("Search"),
                        css_class="btn btn-primary btn-sm",
                    )
                ),
                css_class="d-flex justify-content-evenly",
            ),
        )
