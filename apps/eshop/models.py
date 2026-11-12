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
        # null=True,
        # blank=True
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна происхождения",
        blank=True,
        null=True
    )
    tags = models.ManyToManyField("Tag", related_name='products', blank=True, verbose_name='Теги')
    image = models.ImageField(upload_to="eshop_images/", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Цена")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    status = models.CharField(choices=STATUS_CHOICES, default='published', verbose_name="Статус")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    viewed_by_users = models.ManyToManyField(
        User, related_name='viewed_products',
        blank=True,
        verbose_name="Просмотрено пользователями"
    )
    liked_by_users = models.ManyToManyField(
            User,
            related_name="liked_products",
            blank=True,
            verbose_name="Лайки"
    )
    disliked_by_users = models.ManyToManyField(
        User,
        related_name="disliked_products",
        blank=True,
        verbose_name="Дизлайки"
    )
    favorited_by_users = models.ManyToManyField(
            User,
            related_name="favorited_products",
            blank=True,
            verbose_name="Добавил в избранное"
    )

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
    

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, editable=False)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"
        # db_table = "eshop_tags"

    def get_absolute_url(self):
        return reverse('eshop:tag_products', kwargs={'tag_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.name}'

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    def __str__(self):
        if self.parent:
            parent_text = self.parent.text[:20] + '...' if len(self.parent.text) > 20 else self.parent.text
            reply_text = self.text[:20] + '...' if len(self.text) > 20 else self.text
            return (
                f'Ответ от {self.author} на отзыв  пользователя {self.parent.author}: '
                f'комм. "{parent_text}", отв. "{reply_text}"'
            )
        return f'Комментарий от {self.author} к товару "{self.product}": {self.text if len(self.text) < 20 else self.text[:20] + '...'}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = "комментарии"
        # db_table = "eshop_comments"

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user}'

    @property
    def total_items(self):
        # Общее количество единиц всех товаров в корзине (для счётчика в шапке)
        return sum(item.quantity for item in self.items.all())  # type: ignore

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())  # type: ignore


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'товары в корзине'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product.title} ({self.quantity} шт.)'

    @property
    def total_price(self):
        return self.product.price * self.quantity

