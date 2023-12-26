from django.contrib import admin
from .models import Store, Brand, Category, Product, ProductImages,  ProductsRelated

class StoreAdmin(admin.ModelAdmin):
    list_display = ['name','description','address', 'logo', 'id']    
admin.site.register(Store,StoreAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','image','show']    
admin.site.register(Category,CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','image','start', 'end','show']    
admin.site.register(Brand,BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category', 'price','image', 'show', 'new', 'featured_product']    
admin.site.register(Product,ProductAdmin)

admin.site.register(ProductImages)
admin.site.register(ProductsRelated)

