from typing import Any, Optional
from django.http import HttpRequest

from .conf import settings
from .types import CartSessionDict


def cart_info(request: HttpRequest) -> dict[str, Any]:
    cart_data: Optional[CartSessionDict]
    num_products = 0

    if cart_data := request.session.get(settings.SESSION_KEY_CART):
        num_products = len(cart_data["products"])
    return {"cart_info": {"num_products": num_products}}
