from django.shortcuts import render, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart, CartItem, Order_Product, Order, Payment
from django.http import JsonResponse
import json
from authy.models import NewUser, Address
from django.contrib import messages
from shopify.context_processors import cartProcessor

# Create your views here.
Donation = []


def shop(request):
    product = Product.objects.all()
    return render(request, 'shop/shop-grid.html', {'products': product})


def orderPay(request):
    addressId = request.POST.get('radio')
    address = Address.objects.get(id=addressId)
    user = request.user
    order = Order.objects.create(user=user, address=address, status="1")
    order.save()
    cart = Cart.objects.get(user=request.user, complete=False)
    cartItem = CartItem.objects.filter(cart=cart)
    amt = 0
    for its in cartItem:
        amt += its.amt

        ord_Prod = Order_Product(order=order, qty=its.quantity, product=its.product, amt=its.amt)
        ord_Prod.save()
    order.amt = amt
    order.save()
    orderItem = Order_Product.objects.filter(order=order)
    amt = amt * 100
    client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
    payment = client.order.create({'amount': amt, 'currency': 'INR', 'payment_capture': '1'})
    pay = Payment(order=order, payment_id=payment['id'])
    pay.save()
    context = {
        'order': order,
        'orderItems': orderItem,
        'paymentId': payment['id'],
        'key_id': settings.KEY_ID,
        'address': address

    }
    return render(request, 'shop/razorpay.html', context)


def updateItem(request):
    cartPro = cartProcessor(request)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    product = Product.objects.get(id=productId)
    cartObj, created = Cart.objects.get_or_create(user=request.user, complete=False)

    cartItem, created = CartItem.objects.get_or_create(cart=cartObj, product=product)

    if action == 'add':
        cartItem.quantity = (cartItem.quantity + 1)
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity - 1)
    amt = cartItem.product.price * cartItem.quantity
    cartItem.amt = amt
    cartItem.save()

    if cartItem.quantity <= 0:
        cartItem.delete()

    cartItems = {
        'productId': cartItem.product.id,
        'quantity': cartItem.quantity,
        'amt': cartItem.amt,
        'cartTotal': cartPro['cartTotal'],
        'cartCount': cartPro['cartCount'],

        'productPrice': cartItem.product.price
    }
    return JsonResponse(cartItems)


def cartView(request):
    cart, created = Cart.objects.get_or_create(user=request.user, complete=False)

    cartItem = CartItem.objects.filter(cart=cart)
    total = 0.0
    for item in cartItem:
        total += item.amt
    context = {
        'items': cartItem,
        'total': total
    }
    return render(request, 'shop/cart.html', context)


def prod_view(request, prod_id):
    product = Product.objects.get(id=prod_id)
    cart, created = Cart.objects.get_or_create(user=request.user, complete=False)
    cartItem = CartItem.objects.filter(cart=cart, product=product)
    context = {
        'product': product,
        'cartItems': cartItem
    }

    return render(request, 'shop/product.html', context)


def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user, complete=False)
    cartItem = CartItem.objects.filter(cart=cart)
    amt = 0
    for its in cartItem:
        amt += (its.product.price * its.quantity)

    address = Address.objects.filter(user=request.user)
    amount = amt * 100

    context = {
        'total_amt': amt,
        'cartItems': cartItem,
        'amount': amount,
        'addresses': address,

    }
    return render(request, 'shop/checkout.html', context)


@csrf_exempt
def handleRequest(request):
    response = request.POST
    print(response)
    client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        print('here')
        pay = Payment.objects.get(payment_id=response['razorpay_order_id'])
        pay.successful = True
        pay.save()
        print(pay)
        order = Order.objects.get(id=pay.order.id)
        order.active = True
        order.paid = True
        order.save()
        print(order)
        messages.success(request, 'Payment Completed')
        return redirect('/')
    except Exception as exception:
        print(exception)
        return redirect('/checkout')
