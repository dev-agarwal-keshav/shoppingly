'''from django.shortcuts import render, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart, CartItem, Order_Product, Order, Payment, Category
from django.http import JsonResponse
import json
from authy.models import NewUser, Address

def searchProduct(request):
    if request.method=='POST':
        search=request.POST.get('search')
        category=request.POST.get('category')
        products=Product.objects.filter(name__startswith=search,category__name=category)
        context={
            'products':products,
            'category': Category.objects.all(),
            'sub-category':Category.objects.all()
        }
        return render(request,'shop/shop-grid.html',context)

'''