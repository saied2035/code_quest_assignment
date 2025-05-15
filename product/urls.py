from django.urls import path
from product.views import product_search

urlpatterns = [
    path('', product_search, name='product_search'),
    path('search', product_search, name='product_search'),
]
