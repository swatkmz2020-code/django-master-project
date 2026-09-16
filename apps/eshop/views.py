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
        form = PostForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                product = form.save()
                return redirect('eshop:product_detail', product_id=product.pk)

            
        return render(
                request,
                'eshop/pages/product_form.html',
                {
                    "form": form,
                    "title": "Добавить товар",
                    "h1": "Новый товар",
                    "submit_button_text": "Добавить",
                }
            )


def product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    extra_context = {
        "title": "Редактировать товар",
        "h1": "Редактирование",
        "submit_button_text": "Сохранить",
    }

    if request.method == "POST":
        form = PostForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("eshop:product_detail", product_id=product.pk)
        return render(
            request,
            'eshop/pages/product_form.html',
            context={
                "form": form,
                **extra_context,
            }
        )

    form = PostForm(instance=product)
    return render(
        request,
        'eshop/pages/product_form.html',
        context={
            "form": form,
            **extra_context,
        }
    )