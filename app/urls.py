
# from django.urls import re_path as url
# from django.conf import settings
# from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static
#--------------------------------------

from django.urls import path, include
from . import views

# app_name = 'app'

urlpatterns = [
    path('',views.index, name="index"),
    path('about',views.about, name="about"),
    path('shop',views.shop, name="shop"),
    path('product/<str:slug>',views.product_detail, name="product"),
    path('contact',views.contact, name="contact"),
    
    # Auth URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist_list, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Product CRUD URLs
    path('product/add/', views.add_product, name='add_product'),
    path('product/update/<slug:slug>/', views.update_product, name='update_product'),
    path('product/delete/<slug:slug>/', views.delete_product, name='delete_product'),
    
    # Brand CRUD URLs
    path('brand/add/', views.add_brand, name='add_brand'),
    path('brand/update/<slug:slug>/', views.update_brand, name='update_brand'),
    path('brand/delete/<slug:slug>/', views.delete_brand, name='delete_brand'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
