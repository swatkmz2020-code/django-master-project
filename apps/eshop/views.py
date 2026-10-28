from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
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
    queryset = Product.objects.filter(status="published").select_related('category')
    context_object_name = 'products'
    template_name = 'eshop/pages/product_list.html'


class CategoryProductsView(ListView):
    context_object_name = 'products'
    template_name = 'eshop/pages/category_products.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.objects.filter(category=self.category, status='published')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class ProductsSearchView(ListView):
    template_name = "eshop/pages/products_search.html"
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_performed'] = any(self.request.GET.keys())
        return context

    def get_queryset(self):
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = Product.objects.filter(status="published")
            condition = Q(title__icontains=search_query) | Q(text__icontains=search_query)
            search_in_categories = self.request.GET.get("in_categories") == 'on'
            search_in_tags = self.request.GET.get("in_tags") == 'on'
            if search_in_categories:
                condition |= Q(category__name__icontains=search_query)
            if search_in_tags:
                condition |= Q(tags__name__icontains=search_query)
            return queryset.filter(condition).distinct()
        return Product.objects.none()


class ProductDetailView(DetailView):
    slug_url_kwarg = 'product_slug'
    template_name = 'eshop/pages/product_detail.html'

    def get_queryset(self):
        base_queryset = Product.objects.select_related('category', 'author').prefetch_related(
            'tags', 'liked_by_users', 'disliked_by_users'
        )
        if self.request.user.is_authenticated:
            return base_queryset.filter(
                Q(status="published") | Q(author=self.request.user)
            )
        return base_queryset.filter(status="published")

    def get_object(self, queryset=None):
        product: Product = super().get_object(queryset)  # type: ignore

        user = self.request.user
        session_key = f'product_{product.slug}_viewed'
        
        if not self.request.session.get(session_key, False) and product.author != user:
            Product.objects.filter(pk=product.pk).update(views=F("views") + 1)  # type: ignore
            product.views += 1
            self.request.session[session_key] = True

        if user.is_authenticated and user != product.author:
            product.viewed_by_users.add(user)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        product = self.object  # type: ignore
        
        context['is_liked'] = False
        context['is_disliked'] = False
        
        if user.is_authenticated:
            context['is_liked'] = product.liked_by_users.filter(pk=user.pk).exists()
            context['is_disliked'] = product.disliked_by_users.filter(pk=user.pk).exists()
            
        context['likes_count'] = product.liked_by_users.count()
        context['dislikes_count'] = product.disliked_by_users.count()

        return context


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


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    slug_url_kwarg = 'product_slug'
    form_class = ProductForm
    template_name = 'eshop/pages/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # type: ignore
        
        if request.user != self.object.author:  # type: ignore
            return render(request, 'eshop/pages/not_allowed.html')
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = "Редактировать товар"
        context['h1'] = "Редактирование"
        context['submit_button_text'] = "Сохранить"
        
        context['form'].fields['tags_input'].initial = ", ".join(tag.name for tag in self.object.tags.all())  # type: ignore
        
        return context

    def form_valid(self, form):
        product = form.save()
        product.tags.clear()
        
        raw_tags = form.cleaned_data.get('tags_input') or ''
        
        if isinstance(raw_tags, str):
            tag_names = [t.strip() for t in raw_tags.split(',') if t.strip()]
        else:
            tag_names = raw_tags
            
        for tag_name in tag_names:
            name = tag_name.name if hasattr(tag_name, 'name') else str(tag_name).strip()  # type: ignore
            if name:
                tag, _ = Tag.objects.get_or_create(name=name)
                product.tags.add(tag)
            
        return redirect('eshop:product_detail', product_slug=product.slug)


class ProductRemoveView(LoginRequiredMixin, DeleteView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'eshop/pages/product_remove_confirm.html'
    success_url = reverse_lazy('eshop:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # type: ignore
        if request.user != self.object.author:  # type: ignore
            return render(request, 'eshop/pages/not_allowed.html')
        return super().dispatch(request, *args, **kwargs)


@require_POST
def product_like(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    product = get_object_or_404(Product, pk=pk)
    user = request.user

    if product.author == user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if product.liked_by_users.filter(pk=user.pk).exists():
        product.liked_by_users.remove(user)
        has_liked = False
    else:
        product.liked_by_users.add(user)
        product.disliked_by_users.remove(user)
        has_liked = True

    return JsonResponse({
        'likes_count': product.liked_by_users.count(),
        'dislikes_count': product.disliked_by_users.count(),
        'has_liked': has_liked,
        'has_disliked': product.disliked_by_users.filter(pk=user.pk).exists(),
    })


@require_POST
def product_dislike(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    product = get_object_or_404(Product, pk=pk)
    user = request.user

    if product.author == user:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if product.disliked_by_users.filter(pk=user.pk).exists():
        product.disliked_by_users.remove(user)
        has_disliked = False
    else:
        product.disliked_by_users.add(user)
        product.liked_by_users.remove(user)
        has_disliked = True

    return JsonResponse({
        'likes_count': product.liked_by_users.count(),
        'dislikes_count': product.disliked_by_users.count(),
        'has_liked': product.liked_by_users.filter(pk=user.pk).exists(),
        'has_disliked': has_disliked,
    })
