from django.urls import path
from . import views

# app_name = 'app'

urlpatterns = [
    path('',views.index, name="index"),
       
    path('about',views.about, name="about"),
    path('shop',views.shop, name="shop"),
    path('shop-single/<str:id>',views.shop_single, name="shop-single"),
    path('contact',views.contact, name="contact"),
]
