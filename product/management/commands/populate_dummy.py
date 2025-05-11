import random
from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Brand, Category, NutritionFact, Product, ProductNutrition


class Command(BaseCommand):
    help = "Seed the database with fake products"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1000,
            help='Number of products to create',
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options['count']

        brands = self._create_brands(fake)
        categories = self._create_categories()
        nutrition_facts = self._create_nutrition_facts()

        for _ in range(count):
            product = Product.objects.create(
                name=fake.catch_phrase(),
                brand=random.choice(brands),
                category=random.choice(categories),
            )
            self._add_nutrition_facts(product, nutrition_facts)

        self.stdout.write(self.style.SUCCESS(
            f"✓ Created {count} products with categories, brands, and nutrition facts!"
        ))

    def _create_brands(self, fake):
        names = set(fake.company() for _ in range(20))
        return [Brand.objects.get_or_create(name=name)[0] for name in names]

    def _create_categories(self):
        names = ['Beverages', 'Snacks', 'Fruits', 'Vegetables',
                 'Dairy', 'Bakery', 'Meat', 'Seafood']
        return [Category.objects.get_or_create(name=name)[0] for name in names]

    def _create_nutrition_facts(self):
        defs = [
            ('Calories', 'kcal'),
            ('Protein', 'g'),
            ('Fat', 'g'),
            ('Carbohydrates', 'g'),
            ('Sugar', 'g'),
            ('Sodium', 'mg'),
        ]
        return [NutritionFact.objects.get_or_create(name=n, unit=u)[0] for n, u in defs]

    def _add_nutrition_facts(self, product, facts):
        for nf in random.sample(facts, k=random.randint(3, 5)):
            val = random.uniform(
                50, 500) if nf.name == 'Calories' else random.uniform(0.1, 50)
            ProductNutrition.objects.create(
                product=product,
                nutrition_fact=nf,
                value=round(val, 2)
            )
