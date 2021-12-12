from django import template
from django.http import HttpRequest
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def bsicon(name: str) -> str:
    return mark_safe(f'<i class="bi-{name}" aria-hidden="true"></i>')
