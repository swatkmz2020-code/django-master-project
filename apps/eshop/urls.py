from django.urls import path
from . import views

app_name = "eshop"

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home_page"),
    path('products/', views.ProductListView.as_view(), name="product_list"),
    path('products/load-more/', views.load_more_products_view, name="load_more_products"),
    path('products/category/<slug:category_slug>/', views.CategoryProductsView.as_view(), name="category_products"),
    path('products/tag/<slug:tag_slug>/', views.TagProductsView.as_view(), name="tag_products"),
    path("products/search/", views.ProductsSearchView.as_view(), name="products_search"),
    path('products/add/', views.ProductAddView.as_view(),  name='product_add'),
    path('products/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:product_slug>/edit/', views.ProductEditView.as_view(), name='product_edit'),
    path('products/<slug:product_slug>/remove/', views.ProductRemoveView.as_view(), name="product_remove"),
    path('products/<int:pk>/like/', views.product_like, name="product_like"),
    path('products/<int:pk>/dislike/', views.product_dislike, name="product_dislike"),
    path('products/<int:product_id>/toggle-favorite/', views.product_favorite_toggle_view, name="product_favorite_toggle"),
    path("products/<int:product_id>/comments/add/", views.add_comment_view, name="add_comment"),
    path('products/<int:product_id>/comments/load-more/', views.load_more_comments_view, name="load_more_comments"),
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('products/<int:product_id>/cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', views.cart_increase_view, name='cart_increase'),
    path('cart/decrease/<int:product_id>/', views.cart_decrease_view, name='cart_decrease'),
    path('cart/remove/<int:product_id>/', views.cart_remove_view, name='cart_remove'),
]




