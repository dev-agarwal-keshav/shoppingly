from django.conf import settings
from shop.models import Product, Cart, CartItem


class CartClass(object):
    def __init__(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        self.cartItems = CartItem.objects.filter(cart=cart)

    def cartSize(self):
        qty = 0
        for items in self.cartItems:
            qty += items.quantity
        return qty

    def cartProduct(self):
        yield self.cartItems
