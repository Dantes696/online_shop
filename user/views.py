from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from store.models import Product
from .forms import *
# Create your views here.
from .models import FavoriteProduct, Mail

from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from shop import settings
from .utils import *


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                username=username,
                password=password
            )
            # user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def save_review(request, product_id):
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        review.product_id = product_id
        review.save()
    else:
        return redirect('index')

    product = Product.objects.get(pk=product_id)
    return redirect('product_detail', product.slug)


def save_favorite_product(request, product_slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=product_slug)
    favorite_products = FavoriteProduct.objects.filter(user=user)
    products = [product.product for product in favorite_products]
    if user:
        if product in products:
            fav_product = FavoriteProduct.objects.get(
                user=user, product=product
            )
            fav_product.delete()
            next_page = request.META.get('HTTP_REFERER')
            return redirect(next_page)
        else:
            FavoriteProduct.objects.create(user=user,
                                           product=product)
            next_page = request.META.get('HTTP_REFERER')
            return redirect(next_page)
    else:
        return redirect('login')


def favorite_products(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        favorite_products = FavoriteProduct.objects.filter(user=user)
        products = [product.product for product in favorite_products]

    context = {
        'title': 'Избранные товары',
        'products': products
    }

    return render(request, 'user/fav_products.html', context)


def save_mail(request):
    email = request.POST.get('email')
    user = request.user if request.user.is_authenticated else None
    if user:
        if email:
            Mail.objects.create(mail=email, user=user)
            next_page = request.META.get('HTTP_REFERER')
            return redirect(next_page)
        else:
            return redirect('login')
    else:
        return redirect('login')


@user_passes_test(lambda u: u.is_superuser)
def send_mail_to_customers(request):
    if request.user.is_superuser and request.method == "POST":
        text = request.POST.get('text')
        mail_list = Mail.objects.all()
        for email in mail_list:
            send_mail(
                subject='У нас новая акция !',
                message=text,
                from_email=settings.EMAIL_HOST_PASSWORD,
                recipient_list=[email],
                fail_silently=True
            )

    return render(request, 'user/send_mail.html')


def cart(request):
    cart_info = get_cart_data(request)

    context = {
        'cart_total_price': cart_info['cart_total_price'],
        'order': cart_info['order'],
        'products': cart_info['products']
    }

    return render(request, 'user/cart.html', context)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        return redirect('login')


def clear_cart(request):
    user_cart = CartForAuthenticatedUser(request)
    order = user_cart.get_cart_info()['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        quantity = order_product.quantity
        product = order_product.product
        order_product.delete()
        product.quantity += quantity
        product.save()
    return redirect('cart')


def checkout(request):
    cart_info = get_cart_data(request)

    context = {
        'title': 'Оформление заказа',
        'order': cart_info['order'],
        'items': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm()
    }

    return render(request, 'user/checkout.html', context)