from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликован'),
        ('draft', 'Черновик')
    )

    title = models.CharField(max_length=200, verbose_name="Название")
    image = models.ImageField(upload_to="eshop_images/", null=True, blank=True)
    text = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Цена")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    status = models.CharField(choices=STATUS_CHOICES, default='draft', verbose_name="Статус")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
