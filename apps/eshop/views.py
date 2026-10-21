from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
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

    def get_object(self, queryset=None):
        product: Product = super().get_object(queryset)  # type: ignore
        # Явно задаем тип Product

        user = self.request.user
        # Используем slug вместо id для уникального ключа просмотра в сессии
        session_key = f'product_{product.slug}_viewed'
        
        if not self.request.session.get(session_key, False) and product.author != user:
            # Обновляем просмотры в базе данных по id (так как id у объекта все равно есть)
            Product.objects.filter(id=product.id).update(views=F("views") + 1)  # type: ignore
            product.views += 1
            self.request.session[session_key] = True

        if user.is_authenticated and user != product.author:
            product.viewed_by_users.add(user) # Дубликатов записей не будет

            
        return product


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
        self.object = self.get_object() # type: ignore
        
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
        
        # Получаем данные из поля формы
        raw_tags = form.cleaned_data.get('tags_input') or ''
        
        # Если это строка — делим её по запятым, если уже список — оставляем как есть
        if isinstance(raw_tags, str):
            tag_names = [t.strip() for t in raw_tags.split(',') if t.strip()]
        else:
            tag_names = raw_tags  # Если Django уже вернул список/QuerySet тегов
            
        for tag_name in tag_names:
            # Если в списке лежат объекты Tag, берем их имя, иначе саму строку
            name = tag_name.name if hasattr(tag_name, 'name') else str(tag_name).strip() # type: ignore
            if name:
                tag, _ = Tag.objects.get_or_create(name=name)
                product.tags.add(tag)
            
        return super().form_valid(form)



class ProductRemoveView(DeleteView):
    model = Product
    pk_url_kwarg = 'product_slug'
    template_name = 'eshop/pages/product_remove_confirm.html'
    paginate_by = 3

    # context_object_name = 'product' # Необязательно
    success_url = reverse_lazy('eshop:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() # type: ignore

        if request.user != self.object.author: # type: ignore
                return render(request, 'eshop/pages/not_allowed.html')

        return super().dispatch(request, *args, **kwargs)
