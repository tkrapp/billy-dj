from typing import Optional

from django.http import HttpRequest

from .conf import settings
from .types import CartSessionDict


def get_or_init_cart(request: HttpRequest) -> CartSessionDict:
    cart_data: Optional[CartSessionDict] = request.session.get(settings.SESSION_KEY_CART)
    if cart_data is None:
        cart_data = init_cart()
        request.session[settings.SESSION_KEY_CART] = cart_data

    return request.session[settings.SESSION_KEY_CART]


def init_cart() -> CartSessionDict:
    return {
        "customer_id": None,
        "customer_address_id": None,
        "products": [],
    }
