# products/managers.py

from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from django.db.models import Q, Value
from django.db.models.functions import Lower


class ProductQuerySet(models.QuerySet):
    def smart_search(self, term, sim_threshold=0.1):
        term_lower = term.lower()
        return (
            self
            .annotate(
                name_lower=Lower('name'),
                sim=TrigramSimilarity(Lower('name'), Value(term_lower))
            )
            .filter(
                Q(name_lower__icontains=term_lower)
                | Q(sim__gt=sim_threshold)
            )
            .order_by('-sim')
        )


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def smart_search(self, term, **kwargs):
        return self.get_queryset().smart_search(term, **kwargs)
