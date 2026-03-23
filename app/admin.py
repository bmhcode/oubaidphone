from django.contrib import admin
from .models import Store, Shop, Brand, Category, Product, ProductImages, Profile, Subscription
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class SubscriptionInline(admin.StackedInline):
    model = Subscription
    can_delete = False
    verbose_name_plural = 'Subscription'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, SubscriptionInline)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'about_us', 'address', 'logo']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'category_image', 'is_active']


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'product_image',
        'is_active',
        'shop',
  
    )
 
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'start_date', 'end_date', 'is_active']


class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'address', 'logo', 'email']


admin.site.register(Store, StoreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Shop, ShopAdmin)

