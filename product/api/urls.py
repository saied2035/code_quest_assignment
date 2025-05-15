from django.urls import path
from product.api.views import ProductSearchAPIView

urlpatterns = [
    path('search', ProductSearchAPIView.as_view(), name='product_search_api'),
]
