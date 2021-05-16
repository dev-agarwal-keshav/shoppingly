from django.urls import path
from . import views
urlpatterns=[
    path('login', views.loginpage, name="login page"),
    path('logout', views.user_logout, name="logout page"),
    path('register/', views.registerpage, name="register page"),
    path('logging', views.logging, name="logging in"),
    path('registration', views.registration, name='registration'),
    path('activate/<uidb64>/<token>', views.activateView, name='activate'),
    path('address/submit/',views.addAddress,name="add address")
]