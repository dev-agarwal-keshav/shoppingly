from shop.models import Cart, CartItem


def cartProcessor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartItems = CartItem.objects.filter(cart=cart)
        qty = 0
        total = 0.0
        for items in cartItems:
            qty += items.quantity
            total += items.amt

        return {'cartCount': qty, 'cartList': cartItems, 'cartTotal': total}
    else:
        return None