from django.shortcuts import render

from eshop.models import Product


def home_page_view(request):
    return render(request, template_name='eshop/index.html')


def product_list_view(request):
    products = Product.objects.all()
    return render(request, template_name='eshop/product_list.html', context={'products': products})


