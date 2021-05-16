from seller.models import Seller
from django.shortcuts import render
from shop.models import Product, Order_Product
from .models import Seller
# Create your views here.
def home(request):
    return render(request,'seller/base.html')


def orders(request):
    seller=Seller.objects.get(user=request.user)
    order_item=Order_Product.objects.filter(product__seller=seller)
    context={
        'items':order_item
    }
    return render(request,'seller/orders.html',context)


def products(request):
    seller=Seller.objects.get(user=request.user)
    items=Product.objects.filter(seller=seller)
    context={
        'items':items
    }
    return render(request,'seller/product_list.html',context)