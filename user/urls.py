from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('save_review/<int:product_id>/', save_review, name="save_review"),
    path('add_favorite/<slug:product_slug>/', save_favorite_product, name='add_favorite'),
    path('my_favorites/', favorite_products, name='favorite_products'),
    path('save_mail/', save_mail, name='save_mail'),
    path('send_mail/', send_mail_to_customers, name='send_mail'),

    path('cart/', cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout')


]
