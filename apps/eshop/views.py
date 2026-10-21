from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView
)

from eshop.forms import ProductForm
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


class ProductAddView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    extra_context = {
        "title": "Добавить товар",
        "h1": "Новый товар",
        "submit_button_text": "Добавить"
    }
    template_name = 'eshop/pages/product_form.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.author = self.request.user
        product.save()
                
        tag_names = form.cleaned_data.get('tags_input') or []
                
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            product.tags.add(tag)
                
            return redirect('eshop:product_detail', product_slug=product.slug)

        return redirect('eshop:product_detail', product_slug=product.slug)


class ProductEditView(UpdateView):
    model = Product
    slug_url_kwarg = 'product_slug'
    form_class = ProductForm
    template_name = 'eshop/pages/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Добавляем ignore в конец строки 105
        self.object = self.get_object()  # type: ignore
        
        # Добавляем ignore в конец строки 109
        if request.user != self.object.author:  # type: ignore
            return render(request, 'eshop/pages/not_allowed.html')
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = "Редактировать товар"
        context['h1'] = "Редактирование"
        context['submit_button_text'] = "Сохранить"
        
        # Добавляем ignore в конец строки 120
        context['form'].fields['tags_input'].initial = ", ".join(tag.name for tag in self.object.tags.all())  # type: ignore
        
        return context


    def form_valid(self, form):
        product = form.save()
        product.tags.clear()
        
        raw_tags = form.cleaned_data.get('tags_input') or ''
        tag_names = [t.strip() for t in raw_tags.split(',') if t.strip()]
        
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            product.tags.add(tag)
            
        return super().form_valid(form)


def product_remove_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if request.user != product.author:
        return render(request, 'eshop/pages/not_allowed.html')

    if request.method == "POST":
        product.delete()
        return redirect("eshop:product_list")

    return render(request, 'eshop/pages/product_remove_confirm.html', {'product': product})
