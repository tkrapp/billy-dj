from django.core.management.base import BaseCommand, CommandError
from billy_warehouse import models


class Command(BaseCommand):
    help = "Updates all search documents"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        models.ProductSearch.objects.update_search_documents()
