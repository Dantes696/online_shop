from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:category_slug>/', category_detail, name='category_detail'),
    path('product/<slug:product_slug>/', product_detail, name='product_detail'),


]