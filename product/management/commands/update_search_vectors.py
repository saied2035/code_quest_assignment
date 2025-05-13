# product/management/commands/update_search_vectors.py

from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from product.models import Product

class Command(BaseCommand):
    help = "Bulk update search_vector field for all products"

    def handle(self, *args, **kwargs):
        Product.objects.update(
            search_vector=SearchVector('name', config='english') +
                          SearchVector('name', config='arabic')
        )
        self.stdout.write(self.style.SUCCESS("Updated all search vectors"))
