from typing import Union
from django import forms
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy


def render_crispy_form(
    request: HttpRequest, form: Union[forms.Form, forms.ModelForm]
) -> HttpResponse:
    return render(
        request=request, template_name="shared/crispy_form.html", context={"form": form}
    )


def is_all_digits(value: str):
    if not value.isdecimal():
        raise forms.ValidationError(
            message=gettext_lazy("The field may only contain digits")
        )


class SearchInput(forms.widgets.Input):
    input_type = "search"


class PostalCodeForm(forms.Form):
    q = forms.CharField(
        label=gettext_lazy("Query"), max_length=5, validators=[is_all_digits]
    )
    limit = forms.IntegerField(label=gettext_lazy("Limit"), min_value=1, required=False)


class PaginationForm(forms.Form):
    p = forms.IntegerField(label=gettext_lazy("Page number"), min_value=1, initial=1)

    def get_page_number(self) -> int:
        if self.is_valid():
            return self.cleaned_data["p"]
        return self.fields["p"].initial
