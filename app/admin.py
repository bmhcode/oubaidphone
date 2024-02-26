from django.contrib import admin
from .models import Store, Brand, Category, Product, ProductImages

class StoreAdmin(admin.ModelAdmin):
    list_display = ['name','about_us','address', 'logo', 'id']    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','image','category_image','show']    

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','image','start', 'end','show']    

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['name','category', 'price','image', 'show', 'new', 'featured_product']    

admin.site.register(Store,StoreAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImages)

