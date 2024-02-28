
# from django.urls import re_path as url
# from django.conf import settings
# from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static
#--------------------------------------

from django.urls import path
from . import views

# app_name = 'app'

urlpatterns = [
    
    # url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    # -------------------------------
    path('',views.index, name="index"),
       
    path('about',views.about, name="about"),
    path('shop',views.shop, name="shop"),
    path('product/<str:id>',views.product_detail, name="product-detail"),
    path('contact',views.contact, name="contact"),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
