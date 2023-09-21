from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150,
                             verbose_name='Наименование категории')
    image = models.ImageField(upload_to='photos/categories/',
                              verbose_name='Изображение категории',
                              null=True, blank=True)

    slug = models.SlugField(unique=True, null=True)

    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Категория',
                               related_name='subcategories')

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Категория: pk={self.pk}, title={self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name="Бренд")
    description = models.TextField(verbose_name="Описание бренда")
    image = models.ImageField(verbose_name="Фото бренда",
                              null=True,
                              blank=True)

    def get_photo(self):
        if self.image:
            try:
                return self.image.url
            except:
                return static("store/images/brand_info-img.png")
        else:
            return static("store/images/brand_info-img.png")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Бренд: pk={self.pk}, title={self.title}"

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    price = models.IntegerField(verbose_name='Цена', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(default='Здесь скоро будет описание',
                                   verbose_name='Описание товара')
    size = models.FloatField(default=30.0, verbose_name='Размер в мм')
    color = models.CharField(max_length=150, default='Серебрянный',
                             verbose_name='Цвет')
    material = models.CharField(max_length=150, default='Серебро',
                                verbose_name='Материал')
    slug = models.SlugField(unique=True, null=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='products')
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              verbose_name='Бренд',
                              related_name='brands')

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all().first().image.url
            except:
                return f"""https://avatars.mds.yandex.net/i?id=d96655a5cc1166caf7063bfa36b112437b3bdbf5-7679814-images-thumbs&n=13"""
        else:
            return f"""https://avatars.mds.yandex.net/i?id=d96655a5cc1166caf7063bfa36b112437b3bdbf5-7679814-images-thumbs&n=13"""

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Продукт: pk={self.pk}, title={self.title}, price={self.price}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Gallery(models.Model):
    image = models.ImageField(upload_to='photos/products/',
                              verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')

    def __str__(self):
        return f"""Фото № {self.pk} продукта {self.product.title}"""

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображении'


