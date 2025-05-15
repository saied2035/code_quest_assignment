from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from product.models import Product
from product.api.serializers import ProductSerializer


class ProductSearchAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        q = request.query_params.get('q', '').strip()
        if not q:
            return Response(
                {"detail": "Provide a search term via ?q=…"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        params = self.request.query_params
        term = params.get('q', '').strip()

        return (
            Product.objects
                   .prefetch_related('brands', 'categories')
                   .smart_search(term)
        )
