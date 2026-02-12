from django.contrib import admin
from .models import Store, Brand, Category, Product, ProductImages

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
    list_display = ['name','category','old_price', 'price','image', 'product_image', 'is_active', 'new_product', 'featured_product']    

admin.site.register(Store,StoreAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Product,ProductAdmin)

