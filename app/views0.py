from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Store, Brand, Category, Product, Wishlist
from .forms import ProductForm, BrandForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# ... existing code ...

@login_required
def add_product(request):
    store = _get_store()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('shop')
    else:
        form = ProductForm()
    
    context = {'form': form, 'store': store, 'title': 'Add Product'}
    return render(request, 'app/product_form.html', context)

@login_required
def update_product(request, slug):
    store = _get_store()
    product = get_object_or_404(Product, slug=slug)
    
    # Check if the user is the owner of the product
    if product.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to edit this product.')
        return redirect('shop')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'store': store, 'title': 'Edit Product', 'product': product}
    return render(request, 'app/product_form.html', context)

@login_required
def delete_product(request, slug):
    store = _get_store()
    product = get_object_or_404(Product, slug=slug)
    
    # Check if the user is the owner of the product
    if product.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('shop')

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('shop')
    
    context = {'product': product, 'store': store}
    return render(request, 'app/product_confirm_delete.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_brand(request):
    store = _get_store()
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully!')
            return redirect('about')
    else:
        form = BrandForm()
    
    context = {'form': form, 'store': store, 'title': 'Add Brand'}
    return render(request, 'app/brand_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_brand(request, slug):
    store = _get_store()
    brand = get_object_or_404(Brand, slug=slug)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully!')
            return redirect('about')
    else:
        form = BrandForm(instance=brand)
    
    context = {'form': form, 'store': store, 'title': 'Edit Brand'}
    return render(request, 'app/brand_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_brand(request, slug):
    store = _get_store()
    brand = get_object_or_404(Brand, slug=slug)
    
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand deleted successfully!')
        return redirect('about')
    
    context = {'brand': brand, 'store': store}
    return render(request, 'app/brand_confirm_delete.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    store = _get_store()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('shop')
    else:
        form = CategoryForm()
    
    context = {'form': form, 'store': store, 'title': 'Add Category'}
    return render(request, 'app/category_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_category(request, slug):
    store = _get_store()
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('shop')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'store': store, 'title': 'Edit Category', 'category': category}
    return render(request, 'app/category_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, slug):
    store = _get_store()
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('shop')
    
    context = {'category': category, 'store': store}
    return render(request, 'app/category_confirm_delete.html', context)

def _get_store():
    """
    Retrieves the first Store object from the database.
    If no store exists, it creates a default one.
    """
    store = Store.objects.first()
    if not store:
        store = Store.objects.create(name="My Store", about_us="Welcome to our store!")
    return store

def index(request):
    store = _get_store()
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    context = {
        'store': store,
        'categories': categories,
        'products': products,
        }
    return render(request, 'app/index.html', context)

def shop(request):
    store = _get_store()
    categories = Category.objects.filter(is_active=True)
    # Filter products
    cat_filter = request.GET.get('cat_filter')
    products = Product.objects.filter(is_active=True)
    if cat_filter:
        products = products.filter(category__name=cat_filter)
        
    brands = Brand.objects.filter(is_active=True)
    # Set up Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    product_pages = paginator.get_page(page_number)
    
    # Generate range for pagination (using a range object is cleaner than string multiplication)
    # However, to maintain template compatibility if it iterates over a string:
    nums = "a" * product_pages.paginator.num_pages
    
    context = {
        'store': store,
        'brands': brands,
        'categories': categories,
        'products': products,
        'product_pages': product_pages,
        'nums': nums,
    }
            
    return render(request, 'app/shop.html', context)

def product_detail(request, slug): 
    store = _get_store()
    categories = Category.objects.filter(is_active=True)   
    product = get_object_or_404(Product, slug=slug)
    
    # Optional: Get related products based on category
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(slug=slug)[:4]
    
    context = {
        'store': store, 
        'categories': categories,
        'product': product,
        'related_products': related_products 
    }
    return render(request, 'app/product_detail.html', context)

def about(request):
    store      = _get_store()
    categories = Category.objects.filter(is_active=True)
    brands     = Brand.objects.filter(is_active=True)   # Show the brands
             
    context = {
        'store': store,
        'categories': categories,
        'brands': brands, 
    }
    return render(request, 'app/about.html', context)

def contact(request):
    store = _get_store()
    categories = Category.objects.filter(is_active=True)   
        
    context = {
        'store': store,
        'categories': categories
    }
    return render(request, 'app/contact.html', context)

def signup(request):

    store = _get_store()
    categories = Category.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    
    context = {
        'store': store,
        'categories': categories,
        'form': form
    }
    return render(request, 'registration/signup.html', context)

    # ... existing code ...

@login_required
def wishlist_list(request):
    store = _get_store()
    categories = Category.objects.filter(is_active=True)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    
    context = {
        'store': store,
        'categories': categories,
        'products': products
    }
    return render(request, 'app/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')