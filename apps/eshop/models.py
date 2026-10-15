from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликован'),
        ('draft', 'Черновик')
    )

    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, editable=False)
    category = models.ForeignKey(
        'Category',
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name="Категория",
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна происхождения",
        blank=True,
        null=True
    )

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

    def get_absolute_url(self):
            #     # return f"/products/{self.slug}/"
            #     # return reverse('eshop:product_detail', args=[self.slug])
        return reverse('eshop:product_detail', kwargs={'product_slug': self.slug})


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, editable=False)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = "категории"
        # db_table = "eshop_categories"

    def get_absolute_url(self):
        return reverse('eshop:category_products', kwargs={'category_slug': self.slug})

    # def get_absolute_url(self):
    # #     # return f"/products/{self.slug}/"
    # #     # return reverse('eshop:product_detail', args=[self.slug])
    #     return reverse('eshop:product_detail', kwargs={'product_slug': self.slug})


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name