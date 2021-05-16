'''from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, ),

    path('search/product/',views.searchProduct),

    path('update_item/', views.updateItem, ),
    path('cart/', views.cartView),
    path('product/<int:id>/', views.prod_view),
    path('checkout/', views.checkout),

    path('update/address/', views.addressUpdate),

    path('success/', views.handleRequest)
]
'''