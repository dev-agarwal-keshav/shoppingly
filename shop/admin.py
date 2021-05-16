from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order_Product, Order, Payment
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name',)
    filter_by=('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','category','available')
    filter_by=('price',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=('user','cart_value',)

    def cart_value(self,obj):
        cartItem=CartItem.objects.filter(cart=obj)
        amt=0.0
        for item in cartItem:
            amt+=item.amt
        return amt

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=('cart','product','amt',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('user','amt','status','paid' ,)

@admin.register(Order_Product)
class OrderAdmin(admin.ModelAdmin):
    list_display=('order','product','amt', )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=('order','payment_id','successful', )