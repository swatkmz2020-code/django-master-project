from django.contrib import admin
from .models import Category, Product, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. Добавляем 'get_tags' в список отображения таблицы
    list_display = ('title', 'price', 'category', 'get_tags', 'country')
    fields = ('title', 'category', 'country', 'text', 'tags', 'price', 'image', 'author')


    # 2. Создаем метод, который склеит все теги товара через запятую
    def get_tags(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])
    
    # 3. Красивое название колонки для таблицы
    get_tags.short_description = 'Теги'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
        list_display = ('name', 'slug')



