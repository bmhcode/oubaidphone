from django.contrib import admin
from .models import Store, Brand, Category, Product, ProductImages, Profile

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = ['name','about_us','address', 'logo', 'id']    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','image','category_image','is_active']    

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','image','start', 'end','is_active']    
    

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['name','category', 'price', 'product_image', 'is_active']   
    

admin.site.register(Store,StoreAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Product,ProductAdmin)


