from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class BillyCustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billy_customer'
    verbose_name = gettext_lazy("Customer")
