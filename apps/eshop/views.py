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
        title = request.POST['title'].strip()
        text = request.POST['text'].strip()
        price = request.POST['price'].strip()

        errors = {}
        if not title:
            errors['title'] = 'Название товара обязательно к заполнению.'
        if not text:
            errors['text'] = 'Описание товара обязательно к заполнению.'
        if not price:
            errors['price'] = 'Цена товара обязательна к заполнению.'

        if errors:
            context = {
                'errors': errors,
                'title': title,
                'text': text,
                'price': price
            }
            return render(request, 'eshop/product_add.html', context)

        product = Product.objects.create(title=title, text=text, price=price)
        
        return redirect('eshop:product_detail', product_id=product.pk)
        
    # Все остальные запросы (включая GET) уходят сюда
    return render(request, 'eshop/product_add.html')
