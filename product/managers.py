# products/managers.py

from django.contrib.postgres.search import TrigramSimilarity
from django.db import models

class ProductQuerySet(models.QuerySet):
    def fuzzy(self, term, threshold=0.3):
        return (
            self
            .annotate(similarity=TrigramSimilarity('name', term))
            .filter(similarity__gt=threshold)
            .order_by('-similarity')
        )

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def fuzzy_search(self, term, **kwargs):
        return self.get_queryset().fuzzy(term)
