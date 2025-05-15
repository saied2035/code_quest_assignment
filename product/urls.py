from django.urls import path, include
from product.views import product_search

urlpatterns = [
    path('', product_search, name='product_search'),
    path('search', product_search, name='product_search'),
    path('products/api/', include('product.api.urls')),
]
