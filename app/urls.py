
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
    path('contact',views.contact, name="contact"),
     
#--------------------- Auth -------------------------
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('update_profile',views.update_profile, name="update_profile"),
#--------------------- / Auth -------------------------
    
#--------------------- Store -------------------------
    path('store',views.store, name="store"),
    path('store/settings/', views.update_store, name='update_store'),
    path('store/delete/', views.delete_store, name='delete_store'),
#--------------------- / Store -------------------------

#--------------------- Category -------------------------
    path('category/add/', views.add_category, name='add_category'),
    path('category/update/<slug:slug>/', views.update_category, name='update_category'),
    path('category/delete/<slug:slug>/', views.delete_category, name='delete_category'),
#--------------------- / Category -------------------------

#--------------------- Product -------------------------
    path('product/add/', views.add_product, name='add_product'),
    path('product/update/<slug:slug>/', views.update_product, name='update_product'),
    path('product/delete/<slug:slug>/', views.delete_product, name='delete_product'),
    path('product/<slug:slug>',views.product_detail, name="product_detail"),
#--------------------- / Product -------------------------

#--------------------- Product Images -----------------------
    path('product/<slug:slug>/images/', views.manage_product_images, name='manage_product_images'),
    path('product/<slug:slug>/images/add/', views.add_product_image, name='add_product_image'),
    path('product/images/delete/<int:image_id>/', views.delete_product_image, name='delete_product_image'),
#--------------------- / Product Images -----------------------

#--------------------- Shop --------------------------------
    path('shop/<str:username>/', views.shop, name='shop'),
    path('shop/update/<slug:slug>/', views.update_product, name='update_product'),
    path('shop/delete/<slug:slug>/', views.delete_product, name='delete_product'),
#--------------------- / Shop ------------------------------

#--------------------- Brand -------------------------
    path('brands/', views.brands, name='brands'),
    path('brand/add/', views.add_brand, name='add_brand'),
    path('brand/update/<slug:slug>/', views.update_brand, name='update_brand'),
    path('brand/delete/<slug:slug>/', views.delete_brand, name='delete_brand'),
#--------------------- / Brand -------------------------

#--------------------- Wishlist -------------------------
    path('wishlist/', views.wishlist_list, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
#--------------------- / Wishlist -------------------------

#--------------------- Plan -------------------------
    path("plan/", views.plan, name="plan"),
    path("upgrade-plan/", views.upgrade_plan, name="upgrade_plan"),
#--------------------- / Plan -------------------------
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
