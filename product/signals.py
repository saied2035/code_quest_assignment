from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Product


@receiver(pre_save, sender=Product)
def update_search_vector(_, instance, **kwargs):
    instance.search_vector = (
        SearchVector('name', config='english') +
        SearchVector('name', config='arabic')
    )
