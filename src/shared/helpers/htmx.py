from typing import Optional

from django.http import HttpRequest
from django_htmx.middleware import HtmxDetails


def get_htmx_details(request: HttpRequest) -> Optional[HtmxDetails]:
    if hasattr(request, "htmx"):
        return request.htmx  # type: ignore
    return None
