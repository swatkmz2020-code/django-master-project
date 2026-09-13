from django.shortcuts import get_object_or_404, redirect, render

from eshop.forms import PostForm
from eshop.models import Product


def home_page_view(request):
    return render(request, template_name='eshop/pages/index.html')


def product_list_view(request):
    products = Product.objects.all()
    return render(request, template_name='eshop/pages/product_list.html', context={'products': products})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'eshop/pages/product_detail.html', {'product': product})


def product_add_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            product = Product.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                price=form.cleaned_data['price']
            )
            return redirect('eshop:product_detail', product_id=product.pk)

        return render(request, 'eshop/pages/product_add.html', {"form": form})

    form = PostForm()
    return render(request, 'eshop/pages/product_add.html', {"form": form})
