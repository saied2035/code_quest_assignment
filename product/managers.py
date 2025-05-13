# product/managers.py

from django.db import models
from django.db.models import Q, Value, F
from django.db.models.functions import Lower
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, TrigramSimilarity
)

class ProductQuerySet(models.QuerySet):
    def smart_search(self, term, sim_threshold=0.13):
        term_lower = term.lower()
        query = SearchQuery(term_lower, config='simple')  # supports Arabic + English

        return (
            self.annotate(
                name_lower=Lower('name'),
                sim=TrigramSimilarity(Lower('name'), Value(term_lower)),
                rank=SearchRank(F('search_vector'), query)
            )
            .filter(
                Q(name_lower__icontains=term_lower) |
                Q(sim__gt=sim_threshold) |
                Q(search_vector=query)
            )
            .order_by('-rank', '-sim')
        )

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def smart_search(self, term, **kwargs):
        return self.get_queryset().smart_search(term, **kwargs)
