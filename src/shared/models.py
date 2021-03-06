from __future__ import annotations

from textwrap import dedent
from typing import Any, Generic, Mapping, Optional, Type, TypeVar
from typing_extensions import Self

from django import forms
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models.query import QuerySet
from django.template import Context, Template
from django.utils.translation import gettext, gettext_lazy

from crispy_forms.helper import FormHelper

_T = TypeVar("_T")
_I = TypeVar("_I", bound=models.Model)


class HideableQuerySet(Generic[_I], models.QuerySet):
    def visible(self) -> HideableQuerySet[_I]:
        return self.filter(hidden=False)

    def hidden(self) -> HideableQuerySet[_I]:
        return self.filter(hidden=True)


class HideableManager(models.Manager):
    def visible(self) -> "HideableQuerySet[HideableModel]":
        return self.get_queryset().visible()

    def hidden(self) -> "HideableQuerySet[HideableModel]":
        return self.get_queryset().hidden()

    def get_queryset(self) -> "HideableQuerySet[HideableModel]":
        queryset = HideableQuerySet(self.model)

        if self._db is not None:
            return queryset.using(self._db)
        return queryset.using("default")

    def replace(self, instance: HideableModel, other: HideableModel):
        with transaction.atomic():
            instance.hidden = True
            instance.save()
            other.save()


class HideableModel(models.Model):
    hidden = models.BooleanField(verbose_name=gettext_lazy("Hidden"), default=False)

    def clone(self: _I) -> _I:
        return type(self)(
            **{
                field.name: getattr(self, field.name)
                for field in self._meta.fields
                if field is not self._meta.pk
            }
        )

    def update(self, data: Mapping[str, Any]) -> Self:
        with transaction.atomic():
            clone = self.clone()

            self.hidden = True
            self.save()

            for field, value in data.items():
                setattr(clone, field, value)

            clone.save()

            return clone

    def hide(self):
        with transaction.atomic():
            self.hidden = True
            self.save()

    class Meta:
        abstract = True


class JSONFormDefinitionField(models.JSONField):
    def __init__(
        self, *args, default_form_class: Optional[Type[forms.Form]] = None, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.default_form_class = default_form_class

    def from_db_value(
        self, value, expression, connection
    ) -> Optional[Type[forms.Form]]:
        value = super().from_db_value(value, expression, connection)  # type: ignore
        print(value, expression, connection)
        if value is None and self.default_form_class:
            return self.default_form_class
        elif value is None:
            return value

        return self.build_form(value)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        try:
            self.build_form(value)
        except Exception as exc:
            raise ValidationError(f"Could not build the form. Error: {exc}") from exc

    def build_form(self, value: Mapping[str, Any]) -> Type[forms.Form]:
        class_template = Template(
            """
            class DynamicForm(forms.Form): {% for name, definition in fields.items %}
                {{ name }} = forms.{{ definition.type }}({% for arg, value in definition.args.items %}
                    {{ arg }}={{ value|safe|stringformat:"s" }},{% endfor %}
                )
            {% endfor %}
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.helper = FormHelper()
                    self.helper.form_tag = False
        """
        )
        cmd = dedent(class_template.render(Context({"fields": value}))).strip()
        locals_dict: dict[str, Any] = {}
        exec(
            cmd,
            {
                "forms": forms,
                "gettext": gettext,
                "gettext_lazy": gettext_lazy,
                "FormHelper": FormHelper,
            },
            locals_dict,
        )
        return locals_dict["DynamicForm"]
