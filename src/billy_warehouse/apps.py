from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class BillyWarehouseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "billy_warehouse"
    verbose_name = gettext_lazy("Warehouse")

    def ready(self) -> None:
        from . import signals

        return super().ready()
