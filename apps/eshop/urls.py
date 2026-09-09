from django.urls import path

from . import views

app_name = "eshop"

urlpatterns = [
    path('', views.home_page_view, name="home_page"),
    path('products/', views.product_list_view, name="product_list"),
]