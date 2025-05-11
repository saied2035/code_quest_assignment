from django.db import models
# Create your models here.
# products/models.py


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
        Brand, on_delete=models.PROTECT, related_name='products')
    categories = models.ManyToManyField(
        Category, on_delete=models.PROTECT, related_name='products')
    nutrition_facts = models.ManyToManyField(
        NutritionFact,
        through='ProductNutrition',
        related_name='products',
    )

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
