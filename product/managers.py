# product/managers.py
import re
from django.db import models
from django.db.models import Q, Value, F, Func
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, TrigramSimilarity
)


class ProductQuerySet(models.QuerySet):
    def smart_search(self, term, sim_threshold=0.3):
        term_lower = term.lower().strip()
        unaccented = Func(Value(term_lower), function='unaccent')

        config = self._detect_language_type(term)

        query = SearchQuery(term_lower, config=config)

        return (
            self.annotate(
                name_unaccent=Func(F('name'), function='unaccent'),
                sim=TrigramSimilarity('name_unaccent', unaccented),
                rank=SearchRank(F('search_vector'), query),
            )
            .filter(
                Q(name_unaccent__icontains=term_lower)
                | Q(sim__gt=sim_threshold)
                | Q(search_vector=query)
            )
            .order_by('-rank', '-sim').distinct()
        )

    def _detect_language_type(self, text) -> str:
        arabic_chars = re.compile(r'[\u0600-\u06FF]')
        english_chars = re.compile(r'[A-Za-z]')

        has_arabic = bool(arabic_chars.search(text))
        has_english = bool(english_chars.search(text))
        config = "english"
        if has_arabic and has_english:
            config = "simple"
        elif has_arabic:
            config = "arabic"
        elif has_english:
            config = "english"
        return config


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def smart_search(self, term, **kwargs):
        return self.get_queryset().smart_search(term, **kwargs)
