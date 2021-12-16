from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request=request, template_name="billy_warehouse/index.html", context={}
    )
