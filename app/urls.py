from django.urls import path
from . import views

# app_name = 'app'

urlpatterns = [
    path('',views.index, name="index"),
       
    path('about',views.about, name="about"),
    path('shop',views.shop, name="shop"),
    path('product/<str:id>',views.product_detail, name="product-detail"),
    path('contact',views.contact, name="contact"),
]
