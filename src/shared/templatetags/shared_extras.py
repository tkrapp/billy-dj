from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def is_active_namespace(request: HttpRequest, namespace: str) -> str:
    resolved = request.resolver_match

    if resolved and namespace in set(resolved.namespaces):
        return "active"
    return ""
