from django.shortcuts import render
from django.core.paginator import Paginator
from product.models import Product


def product_search(request):
    q = request.GET.get('q', '').strip()

    results = Product.objects.none()
    if q:
        results = Product.objects.smart_search(q)

    # paginate at 10 per page
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/search.html', {
        'q': q,
        'page_obj': page_obj,
    })
