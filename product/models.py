from django.db import models
from .managers import ProductManager
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class NutritionFact(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=20)  # e.g. 'kcal', 'g', 'mg'

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Product(models.Model):
    name = models.CharField(max_length=200)
    brands = models.ManyToManyField(
        Brand, related_name='products')
    categories = models.ManyToManyField(
        Category, related_name='products')
    nutrition_facts = models.ManyToManyField(
        NutritionFact,
        through='ProductNutrition',
        related_name='products',
    )
    search_vector = SearchVectorField(null=True)

    objects = ProductManager()

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]

    def __str__(self):
        return f"{self.name}"


class ProductNutrition(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    nutrition_fact = models.ForeignKey(NutritionFact, on_delete=models.CASCADE)
    value = models.FloatField(
        help_text="Amount in the unit specified on NutritionFact")

    class Meta:
        unique_together = ('product', 'nutrition_fact')

    def __str__(self):
        return (
            f"{self.product.name} – {self.nutrition_fact.name}: "
            f"{self.value}{self.nutrition_fact.unit}"
        )
