from user.models import FavoriteProduct

from django import template


register = template.Library()


@register.simple_tag()
def get_favorite_products(user):
    favorite_products = FavoriteProduct.objects.filter(user=user)
    products = [product.product for product in favorite_products]

    return products