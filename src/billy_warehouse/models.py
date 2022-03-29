from typing import Callable, Iterable, Optional, cast

from django.db import models
from django.template.loader import render_to_string
from django.utils import module_loading
from django.utils.translation import gettext, gettext_lazy
from model_utils.models import TimeStampedModel
from shared.models import HideableManager, HideableModel, JSONFormDefinitionField


class SqliteMatchLookup(models.Lookup):
    lookup_name = "match"

    def as_sqlite(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params

        return f"{lhs} MATCH {rhs}", params

    def as_sql(self, compile, connection):
        raise NotImplementedError(f"Match is not implemented for {connection}")


models.CharField.register_lookup(SqliteMatchLookup)
models.TextField.register_lookup(SqliteMatchLookup)


class Vendor(TimeStampedModel):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"), max_length=100, unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Vendor")
        verbose_name_plural = gettext_lazy("Vendors")
        ordering = ["name"]


class CategoryManager(models.Manager):
    def get_queryset(self) -> models.QuerySet["Category"]:
        return super().get_queryset()


class Category(TimeStampedModel):
    name = models.CharField(
        verbose_name=gettext_lazy("Name"), max_length=100, unique=True
    )
    details_form = models.CharField(
        verbose_name=gettext_lazy("Attributes form class"),
        null=True,
        blank=True,
        max_length=255,
    )
    details_template = models.CharField(
        verbose_name=gettext_lazy("Details template path"),
        help_text=gettext_lazy("Used in products overview"),
        null=True,
        blank=True,
        max_length=255,
    )
    search_document_generator = models.CharField(
        verbose_name=gettext_lazy("Function to generate the search document"),
        help_text=gettext_lazy(
            "This function should return a string containing words for the search index (Callable[[Product], str])"
        ),
        null=True,
        blank=True,
        max_length=255,
    )

    objects: CategoryManager = CategoryManager()

    def __str__(self) -> str:
        return gettext(self.name)

    class Meta:
        verbose_name = gettext_lazy("Category")
        verbose_name_plural = gettext_lazy("Categories")
        ordering = ["name"]


class ProductManager(HideableManager):
    def visible(self) -> models.query.QuerySet["Product"]:
        return cast(models.query.QuerySet[Product], super().visible())

    def hidden(self) -> models.query.QuerySet["Product"]:
        return cast(models.query.QuerySet[Product], super().hidden())


class Product(HideableModel, TimeStampedModel):
    name = models.CharField(verbose_name=gettext_lazy("Name"), max_length=255)
    category = models.ForeignKey(
        to=Category,
        verbose_name=gettext_lazy("Category"),
        on_delete=models.RESTRICT,
    )
    vendor = models.ForeignKey(
        to=Vendor, verbose_name=gettext_lazy("Vendor"), on_delete=models.RESTRICT
    )
    netto_price = models.DecimalField(
        verbose_name=gettext_lazy("Netto price (in Euro)"),
        max_digits=20,
        decimal_places=2,
    )
    details = models.JSONField(verbose_name=gettext_lazy("Details"))
    search_document = models.TextField(
        verbose_name=gettext_lazy("Search document"), default=""
    )

    objects: ProductManager = ProductManager()

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        search_document_generators = {}

        if self.category.search_document_generator and (
            func := module_loading.import_string(
                self.category.search_document_generator
            )
        ):
            search_document_generators = {self.category.pk: func}

        self.search_document = self.generate_search_document(search_document_generators)

        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f"({self.vendor.name}) {self.name}"

    def render_details(self) -> str:
        return render_to_string(
            (self.category.details_template or "billy_warehouse/default_details.html"),
            {"details": self.details},
        )

    def generate_search_document(
        self, search_document_generators: dict[int, Callable[["Product"], str]]
    ) -> str:
        additional_search_document = ""
        if search_document_generator := search_document_generators.get(
            self.category.pk
        ):
            additional_search_document = search_document_generator(self)

        return (
            " ".join(
                [
                    self.name,
                    self.category.name,
                    self.vendor.name,
                ]
            )
            + f" {additional_search_document}"
        )

    class Meta:
        verbose_name = gettext_lazy("Product")
        verbose_name_plural = gettext_lazy("Products")
        ordering = ["name", "category__name", "vendor__name"]


class Stock(TimeStampedModel):
    product = models.ForeignKey(
        to=Product, verbose_name=gettext_lazy("Product"), on_delete=models.RESTRICT
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=gettext_lazy("Quantity"))

    class Meta:
        verbose_name = gettext_lazy("Stock")
        verbose_name_plural = gettext_lazy("Stocks")


class ProductSearchManager(models.Manager):
    def update_search_documents(self) -> None:
        search_document_generators = {
            category.pk: module_loading.import_string(
                category.search_document_generator
            )
            for category in Category.objects.filter(
                ~models.Q(search_document_generator=None)
            )
        }

        for product in Product.objects.visible().select_for_update():
            product.search_document = product.generate_search_document(
                search_document_generators
            )
            product.save()

    def visible(self) -> models.query.QuerySet["ProductSearch"]:
        return super().get_queryset().filter(product__hidden=False)

    def hidden(self) -> models.query.QuerySet["ProductSearch"]:
        return super().get_queryset().filter(product__hidden=True)


class ProductSearch(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, primary_key=True, db_column="rowid"
    )
    search_document = models.TextField(verbose_name=gettext_lazy("Search document"))

    objects: ProductSearchManager = ProductSearchManager()

    def __str__(self) -> str:
        return str(self.product)

    class Meta:
        managed = False
