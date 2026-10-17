from django.urls import path
from . import views

app_name = "eshop"

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home_page"),
    path('products/', views.ProductListView.as_view(), name="product_list"),
    path('products/category/<slug:category_slug>/', views.CategoryProductsView.as_view(), name="category_products"),
    path('products/tag/<slug:tag_slug>/', views.TagProductsView.as_view(), name="tag_products"),
    path('products/add/', views.product_add_view, name='product_add'),
    path('products/<slug:product_slug>/', views.product_detail_view, name='product_detail'),
    path('products/<int:product_id>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<int:product_id>/remove/', views.product_remove_view, name="product_remove"),
]

