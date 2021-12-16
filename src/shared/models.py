from typing import TypeVar
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy


_T = TypeVar("_T")


class HideableManager(models.Manager):
    def visible(self) -> QuerySet:
        return super().get_queryset().filter(hidden=False)

    def hidden(self) -> QuerySet:
        return super().get_queryset().filter(hidden=True)


class HideableModel(models.Model):
    hidden = models.BooleanField(verbose_name=gettext_lazy("Hidden"), default=False)

    class Meta:
        abstract = True
