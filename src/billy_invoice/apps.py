from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class BillyInvoiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "billy_invoice"
    verbose_name = gettext_lazy("Invoice")
