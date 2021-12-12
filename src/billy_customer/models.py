from django.db import models
from django.urls.base import reverse
from django.utils.translation import gettext_lazy

from model_utils.models import TimeStampedModel


class Address(TimeStampedModel):
    address_1 = models.CharField(verbose_name=gettext_lazy("Address 1"), max_length=100)
    address_2 = models.CharField(
        verbose_name=gettext_lazy("Address 2"), max_length=100, blank=True
    )
    address_3 = models.CharField(
        verbose_name=gettext_lazy("Address 3"), max_length=100, blank=True
    )
    city = models.CharField(verbose_name=gettext_lazy("City"), max_length=100)
    postal_code = models.CharField(
        verbose_name=gettext_lazy("Postal code"), max_length=5
    )

    def __str__(self) -> str:
        street = ",".join(
            field for field in [self.address_1, self.address_2, self.address_3] if field
        )
        return f"{street}, {self.postal_code} {self.city}"

    class Meta:
        verbose_name = gettext_lazy("Address")
        verbose_name_plural = gettext_lazy("Addresses")


class Customer(TimeStampedModel):
    name = models.CharField(verbose_name=gettext_lazy("Name"), max_length=255)
    addresses = models.ManyToManyField(to=Address, verbose_name=gettext_lazy("Address"))

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("billy_customer:details", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = gettext_lazy("Customer")
        verbose_name_plural = gettext_lazy("Customers")
