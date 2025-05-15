from django.db.models.signals import pre_save
from django.db.models import Func, Value
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Product


@receiver(pre_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    _ = sender  # noqa: F841 pylint: disable=unused-variable
    instance.search_vector = (
        SearchVector(Func(Value(instance.name), function='unaccent'), config='english') +
        SearchVector(Func(Value(instance.name),
                     function='unaccent'), config='arabic')
    )
