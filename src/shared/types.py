from typing import Optional
from django.http import HttpRequest
from django_htmx.middleware import HtmxDetails


def get_htmx_details(request: HttpRequest) -> Optional[HtmxDetails]:
    return getattr(request, "htmx", None)
