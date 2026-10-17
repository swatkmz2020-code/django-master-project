from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import  DetailView, ListView, TemplateView

from eshop.forms import PostForm
from eshop.models import Category, Product, Tag

class HomePageView(TemplateView):
    template_name = 'eshop/pages/index.html'


class ProductListView(ListView):
    queryset = Product.objects.filter(status="published")
    context_object_name = 'products'
    template_name = 'eshop/pages/product_list.html'


class CategoryProductsView(ListView):
    context_object_name = 'products'
    template_name = 'eshop/pages/category_products.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.objects.filter(category=self.category, status='published')
        # return self.category.products.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagProductsView(ListView):
    context_object_name = 'products'
    template_name = 'eshop/pages/tag_products.html'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Product.objects.filter(tags=self.tag, status='published')
        # return self.tag.products.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class ProductDetailView(DetailView):
    # model = Product # Необязательно
    slug_url_kwarg = 'product_slug'
    template_name = 'eshop/pages/product_detail.html'
    # context_object_name = 'product' # Необязательно
    # slug_field = 'slug' # Необязательно

    def get_queryset(self):
        # Товар доступен, если он опубликован или если текущий пользователь является его автором
        if self.request.user.is_authenticated:
            return Product.objects.filter(
                Q(status="published") | Q(author=self.request.user)
            )
        return Product.objects.filter(status="published")


@login_required
def product_add_view(request):
        form = PostForm(request.POST or None, request.FILES or None)

        if request.method == "POST":
            if form.is_valid():
                product = form.save(commit=False)
                product.author = request.user
                product.save()

            tag_names = form.cleaned_data.get('tags_input') or []

            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                product.tags.add(tag)

                return redirect('eshop:product_detail', product_slug=product.slug)

            
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

    if request.user != product.author:
        return render(request, 'eshop/pages/not_allowed.html')

    extra_context = {
        "title": "Редактировать товар",
        "h1": "Редактирование",
        "submit_button_text": "Сохранить",
    }

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            product.tags.clear()
            tag_names = form.cleaned_data.get('tags_input') or []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                product.tags.add(tag)

            return redirect("eshop:product_detail", product_slug=product.slug)
        return render(
            request,
            'eshop/pages/product_form.html',
            context={
                "form": form,
                **extra_context,
            }
        )

    existing_tags = ", ".join(tag.name for tag in product.tags.all())
    form = PostForm(instance=product, initial={'tags_input': existing_tags})
    return render(
        request,
        'eshop/pages/product_form.html',
        context={
            "form": form,
            **extra_context,
        }
    )

def product_remove_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user != product.author:
        return render(request, 'eshop/pages/not_allowed.html')

    if request.method == "POST":
        product.delete()
        return redirect("eshop:product_list")

    return render(request, 'eshop/pages/product_remove_confirm.html', {'product': product})
