from typing import Any, Mapping
from django.http import HttpResponse


def update_headers(response: HttpResponse, headers: Mapping[str, Any]) -> HttpResponse:
    for header, value in headers.items():
        response.headers[header] = value

    return response
