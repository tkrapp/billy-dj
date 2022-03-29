from typing import MutableSequence, Optional, TypedDict

from django.db import models


class ProductSessionDict(TypedDict):
    product_id: int
    netto_price: float
    quantity: float


class CartSessionDict(TypedDict):
    customer_id: Optional[int]
    customer_address_id: Optional[int]
    products: MutableSequence[ProductSessionDict]


class VATChoices(models.IntegerChoices):
    NINETEEN = 19
    SEVEN = 7
