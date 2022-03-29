from decimal import Decimal

import typed_app_settings


@typed_app_settings.typed_settings_dict("BILLY_INVOICE")
class Settings:
    VAT_CHOICES = [
        (19, "19%"),
        (7, "7%"),
    ]
    SESSION_KEY_CART = "cart"

settings = Settings()
