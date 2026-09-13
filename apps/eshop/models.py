from django.db import models
from decimal import Decimal

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    text = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Цена")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'eshop_products'

    def __str__(self):
        return self.title