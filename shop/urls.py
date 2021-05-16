from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, ),

    path('update_item/', views.updateItem, ),
    path('cart/', views.cartView),
    path('product/<int:prod_id>/', views.prod_view),
    path('checkout/', views.checkout),

    path('order/pay/', views.orderPay),

    path('success/', views.handleRequest)
]
