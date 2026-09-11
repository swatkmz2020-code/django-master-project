from django.shortcuts import get_object_or_404, redirect, render

from eshop.models import Product


def home_page_view(request):
    return render(request, template_name='eshop/index.html')


def product_list_view(request):
    products = Product.objects.all()
    return render(request, template_name='eshop/product_list.html', context={'products': products})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'eshop/product_detail.html', {'product': product})


def product_add_view(request):
    if request.method == "POST":
        product = Product.objects.create(
            title=request.POST['title'],
            text=request.POST['text'],
            price=request.POST.get('price', '0.00')
        )
        return redirect('eshop:product_detail', product_id=product.pk)
        
    # Все остальные запросы (включая GET) уходят сюда
    return render(request, 'eshop/product_add.html')
