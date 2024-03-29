from django.shortcuts import render, get_object_or_404, redirect , reverse
from django.core.paginator import Paginator
from .models import  Store, Brand, Category, Product, ProductImages
# Create your views here.

def index(request):
    store      = Store.objects.get_or_create()
    store      = Store.objects.get(id=1)
    categories = Category.objects.all()#[0:2]
    products   = Product.objects.filter(show = True)
    
    context = {'store' : store, 'categories' : categories,
               'products' : products
               }
    return render(request, 'index.html', context)

def shop(request):
    store      = Store.objects.get(id=1)
    brands     = Brand.objects.filter(show=True)
    categories = Category.objects.filter(show=True)
    
    category = request.GET.get('category')
    if category == None:
        products = Product.objects.filter(show=True)
    else:
        products = Product.objects.filter(category__name = category, show=True)
    
    # Set up Pagination
    p = Paginator(products, 9)
    page = request.GET.get('page')
    product_pages = p.get_page(page)
    nums = "a" * product_pages.paginator.num_pages
    
    context = {'store' : store,
            'brands' : brands,
            'categories' : categories,
            'products' : products,
            'product_pages' : product_pages,
            'nums' : nums,
            'lib_category' : category}
            
    return render(request, 'shop.html', context)


def product_detail(request,id): 
    store = Store.objects.get(id=1)
    
    categories = Category.objects.all()   
    product = Product.objects.get(id=id) #  product = get_object_or_404(Product, id=pid)
    productImages = ProductImages.objects.filter(product_id=id)
    
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    context = {'store' : store, 'categories' : categories,
                'product' : product,
                'productImages' : productImages,
                'related_products' : related_products }
    
    return render(request,'product_detail.html',context)

def about(request):
    store = Store.objects.get(id=1)
    brands     = Brand.objects.filter(show=True)
    categories = Category.objects.all()           
    context = {'store' : store, 'brands' : brands, 'categories' : categories }
    return render(request, 'about.html', context)

def contact(request):
    store = Store.objects.get(id=1)
    categories = Category.objects.all()   
        
    context = {'store' : store, 'categories' : categories 
            }
    return render(request, 'contact.html', context)