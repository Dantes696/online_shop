from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import *
from user.models import Review
from user.forms import ReviewForm
# Create your views here.


def index(request):
    context = {
        'title': "TOTEMBO: Главная страница"
    }

    return render(request, 'store/index.html', context)


def category_detail(request, category_slug):
    main_category = Category.objects.get(slug=category_slug)
    subcategories = main_category.subcategories.all()
    data = Product.objects.filter(category__in=subcategories)
    colors = []
    materials = []

    paged_products = Paginator(data, 4)
    page = request.GET.get("page")
    result = paged_products.get_page(page)

    for product in data:
        if product.color not in colors:
            colors.append(product.color)
        if product.material not in materials:
            materials.append(product.material)

    context = {
        'title': f"Category: {main_category.title}",
        'products': result,
        'colors': colors,
        'materials': materials,
        'subcategories': subcategories,
        'main_category': main_category
    }

    color_fields = request.GET.get('color')

    if color_fields:
        context['products'] = Product.objects.filter(
            color__icontains=color_fields
        )

    material_fields = request.GET.get('material')

    if material_fields:
        context['products'] = Product.objects.filter(
            material__icontains=material_fields
        )

    sort_fields = request.GET.get('sort')

    if sort_fields:
        if sort_fields == 'new':
            context['products'] = Product.objects.all().order_by('-created_at')
        elif sort_fields == 'min_price':
            context['products'] = Product.objects.all().order_by('price')
        elif sort_fields == 'max_price':
            context['products'] = Product.objects.all().order_by('-price')

    subcategory_fields = request.GET.get('subcategory')

    if subcategory_fields:
        category = Category.objects.get(title=subcategory_fields)
        category_id = category.pk
        context['products'] = Product.objects.filter(category=category_id)

    return render(request, 'store/category_detail.html', context)


def product_detail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    category = Category.objects.get(title=product.category.title)
    reviews = Review.objects.filter(product__slug=product_slug)

    context = {
        'title': f'Товар: {product.title}',
        'product': product,
        'main_category': category.parent,
        'reviews': reviews
    }
    if request.user.is_authenticated:
        context['review_form'] = ReviewForm()

    return render(request, 'store/product_detail.html', context)


