from django.contrib import admin
from eshop.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Оставляем slug в общем списке (здесь он разрешен)
    list_display = ('title', 'price', 'category', 'country')
    
    # Удаляем 'slug' из списка редактируемых полей формы
    fields = ('title', 'category', 'country', 'text', 'price', 'image', 'author')


