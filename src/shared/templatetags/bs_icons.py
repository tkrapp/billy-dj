from django import template

from ..helpers.bs_icons import bsicon as _bsicon

register = template.Library()


@register.simple_tag
def bsicon(name: str) -> str:
    return _bsicon(name)
