# product/managers.py
import re
from django.db import models
from django.db.models import Q, Value, F
from django.db.models.functions import Lower
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, TrigramSimilarity
)


class ProductQuerySet(models.QuerySet):
    def smart_search(self, term, sim_threshold=0.3):
        term_lower = term.lower()

        language_type = self._detect_language_type(term)

        if language_type == "arabic":
            config = "arabic"
        elif language_type == "english":
            config = "english"
        else:
            config = "simple"

        query = SearchQuery(term_lower, config=config)

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

    def _detect_language_type(self, text) -> str:
        arabic_chars = re.compile(r'[\u0600-\u06FF]')
        english_chars = re.compile(r'[A-Za-z]')

        has_arabic = bool(arabic_chars.search(text))
        has_english = bool(english_chars.search(text))

        if has_arabic and has_english:
            return "mixed"
        elif has_arabic:
            return "arabic"
        elif has_english:
            return "english"
        else:
            return "unknown"


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def smart_search(self, term, **kwargs):
        return self.get_queryset().smart_search(term, **kwargs)
