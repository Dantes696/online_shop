from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category',
                    'quantity', 'price', 'size',
                    'color', 'material', 'created_at',
                    'get_photo')
    list_editable = ('price', 'quantity', 'size', 'color', 'material')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    inlines = [GalleryInline]

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f"<img src='{obj.images.all()[0].image.url}' width='50'>")
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


admin.site.register(Gallery)
admin.site.register(Brand)

admin.site.unregister(User)
admin.site.unregister(Group)
