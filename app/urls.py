
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
    path('update-profile/<str:username>/',views.update_profile, name="update_profile"),
#--------------------- / Auth -------------------------
    
    
#--------------------- Store -------------------------
    path('store/settings/', views.update_store, name='update_store'),
    path('store/delete/', views.delete_store, name='delete_store'),
    path('products',views.list_products, name="list_products"),
#--------------------- / Store -------------------------


#--------------------- Shop --------------------------------
    path('shops/', views.list_shops, name='list_shops'),

    path('shop/create/', views.create_shop, name='create_shop'),
    path('shop/update/<slug:slug>/', views.update_shop, name='update_shop'),
    path('shop/delete/<slug:slug>/', views.delete_shop, name='delete_shop'),
    path('shop/<slug:shop_slug>/', views.shop, name='shop'),
#--------------------- / Shop ------------------------------


#--------------------- Category -------------------------
    path('categories/', views.list_categories, name='list_categories'),
    
    path('category/add/', views.add_category, name='add_category'),
    path('category/update/<slug:slug>/', views.update_category, name='update_category'),
    path('category/delete/<slug:slug>/', views.delete_category, name='delete_category'),
#--------------------- / Category -------------------------

#--------------------- Product -------------------------
    path("product/add/<slug:shop_slug>/", views.add_product, name="add_product"),
    path('product/update/<slug:slug>/', views.update_product, name='update_product'),
    path('product/delete/<slug:slug>/', views.delete_product, name='delete_product'),
    path('product/<slug:slug>',views.product_detail, name="product_detail"),
#--------------------- / Product -------------------------

#--------------------- Product Images -----------------------
    path('product/<slug:slug>/images/', views.manage_product_images, name='manage_product_images'),
    path('product/<slug:slug>/images/add/', views.add_product_image, name='add_product_image'),
    path('product/images/delete/<int:image_id>/', views.delete_product_image, name='delete_product_image'),
#--------------------- / Product Images -----------------------


#--------------------- Brand -------------------------
    path('brands/', views.brand_list, name='brand_list'),
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

#--------------------- Members -------------------------
    path('user/add/', views.add_user, name='add_user'),
    path('members/', views.list_members, name='list_members'),
#--------------------- / Members -------------------------

#--------------------- Cart -------------------------
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),


    path('cart/update/<int:product_id>/<str:action>/', views.cart_update, name='cart_update'),
#--------------------- / Cart -------------------------

#--------------------- Orders -------------------------
    path('order/create/', views.order_create, name='order_create'),

    path('order/detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/update/<int:pk>/', views.order_update, name='order_update'),
    path('order/delete/<int:pk>/', views.order_delete, name='order_delete'),

    path('order-item/<int:pk>/status/<str:status>/', views.order_item_status, name='order_item_status'),
    path('order/<int:pk>/status/<str:status>/', views.order_status, name='order_status'),

    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:userid>', views.orders_list, name='orders_list_user'),

    path('orders/items/', views.orders_items_list, name='orders_items_list'),
    path('orders/items/<slug:shop_slug>/', views.orders_items_list, name='orders_items_list_shop'),
    # path('orders/items/<int:userid>', views.orders_items_list_user, name='orders_items_list_user'),


#--------------------- / Orders -------------------------   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
