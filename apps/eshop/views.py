from django.shortcuts import get_object_or_404, redirect, render

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
        title = request.POST['title'].strip()
        text = request.POST['text'].strip()
        price = request.POST['price'].strip()

        errors = {}
        if not title:
            errors['title'] = 'Название товара обязательно к заполнению.'
        elif len(title) < 6:
            errors['title'] = 'Название товара должно содержать минимум 6 символов.'
        if not text:
            errors['text'] = 'Описание товара обязательно к заполнению.'
        if not price:
            errors['price'] = 'Цена товара обязательна к заполнению.'
        else:
            try:
                # Переводим в число для проверки (учитываем запятые)
                price_num = float(price.replace(',', '.'))
                if price_num <= 0:
                    errors['price'] = 'Цена товара должна быть больше 0.'
            except ValueError:
                errors['price'] = 'Введите корректное число для цены.'

        if errors:
            context = {
                'errors': errors,
                'title': title,
                'text': text,
                'price': price
            }
            return render(request, 'eshop/pages/product_add.html', context)

        product = Product.objects.create(title=title, text=text, price=price)
        
        return redirect('eshop:product_detail', product_id=product.pk)
        
    # Все остальные запросы (включая GET) уходят сюда
    return render(request, 'eshop/pages/product_add.html')
