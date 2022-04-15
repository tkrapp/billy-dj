from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class CustomizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customization"
    verbose_name = gettext_lazy("Customization")
