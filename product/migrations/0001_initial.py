

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NutritionFact',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('unit', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('brands', models.ManyToManyField(
                    related_name='products', to='product.brand')),
                ('categories', models.ManyToManyField(
                    related_name='products', to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductNutrition',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(
                    help_text='Amount in the unit specified on NutritionFact')),
                ('nutrition_fact', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='product.nutritionfact')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'unique_together': {('product', 'nutrition_fact')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='nutrition_facts',
            field=models.ManyToManyField(
                related_name='products', through='product.ProductNutrition',
                to='product.nutritionfact'),
        ),
    ]
