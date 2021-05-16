from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('orders',views.orders),
    path('product',views.products),
]
