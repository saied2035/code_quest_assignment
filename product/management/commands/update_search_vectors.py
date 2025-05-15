# product/management/commands/update_search_vectors.py
from django.db.models import Func, F
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from product.models import Product


class Command(BaseCommand):
    help = "Bulk update search_vector field for all products"

    def handle(self, *args, **kwargs):
        products = Product.objects.annotate(
            search_vector_combined=(
                SearchVector(Func(F('name'), function='unaccent'),
                             config='english')
                + SearchVector(Func(F('name'), function='unaccent'),
                               config='arabic')
            )
        )

        for product in products:
            Product.objects.filter(pk=product.pk).update(
                search_vector=product.search_vector_combined)

        self.stdout.write(self.style.SUCCESS("Updated all search vectors"))
