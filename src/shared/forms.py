from typing import TypeVar, Union
from django import forms
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def render_crispy_form(
    request: HttpRequest, form: Union[forms.Form, forms.ModelForm]
) -> HttpResponse:
    return render(
        request=request, template_name="shared/crispy_form.html", context={"form": form}
    )
