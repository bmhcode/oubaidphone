from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Store, Category, Product, ProductImages, Subscription, Brand, Wishlist
from django.contrib.auth.models import User
from .forms import StoreForm, ProductForm, BrandForm, CategoryForm, ProductImageForm,  UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def index(request): # index page
  
    
    products = Product.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'brands': brands,
    }
    return render(request, 'app/index.html', context) 
  
def about(request): # about page
   
    brands     = Brand.objects.filter(is_active=True)   # Show the brands
             
    context = {
        'brands': brands, 
    }
    return render(request, 'app/about.html', context)

def contact(request):# contact page
    context = {}
    return render(request, 'app/contact.html', context)

#--------------------- Store -------------------------
def _get_store():
    """
    Retrieves the first store object from the database.
    If no store exists, it creates a default one.
    """
    store = Store.objects.first()
    if not store:
        store = Store.objects.create(name="Store", about_us="Welcome to the store!")
    return store

def store(request): # store list

    products = Product.objects.filter(is_active=True)
    products_total = products.count()

     # search
    search = request.GET.get("search")
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # filter 
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)

    sort = request.GET.get("sort")

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "new":
        products = products.order_by("-created_at")
    # /filter

    # pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    product_pages = paginator.get_page(page_number)
    nums = "a" * product_pages.paginator.num_pages

    brands = Brand.objects.filter(is_active=True)
    context = {
        "products_total": products_total,
        
        "current_sort": sort or "",
        "current_category": category_filter or "",

        'products': product_pages,
        'product_pages': product_pages,
        'nums': nums,

        'brands': brands,
    }
   
    return render(request, 'app/store.html', context)


@login_required # update store
@user_passes_test(lambda u: u.is_superuser)
def update_store(request):
    store = _get_store()
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated successfully!')
            return redirect('index')
    else:
        form = StoreForm(instance=store)
    context = {'form': form, 'title': 'Store settings'}
    return render(request, 'app/store_form.html', context)

@login_required # delete store
@user_passes_test(lambda u: u.is_superuser)
def delete_store(request):
  
    if request.method == 'POST':
        store.delete()
        messages.success(request, 'Store deleted successfully!')
        return redirect('index')
    context = {'store': store}
    return render(request, 'app/store_confirm_delete.html', context)
#--------------------- / Store -------------------------


#--------------------- Auth --------------------------------
def signup(request): # signup
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    
    context = {
            'form': form
    }
    return render(request, 'registration/signup.html', context)

@login_required # update_profile
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('index')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/update_profile.html', context)
#--------------------- / Auth --------------------------------


#--------------------- Plan --------------------------------
def plan(request): # plan
    context = {}
    return render(request, 'app/plan.html', context)

@login_required # upgrade_plan
@user_passes_test(lambda u: u.is_superuser)
def upgrade_plan(request):
    # تأكد أن المستخدم عنده اشتراك
    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        defaults={"plan": "FREE"}
    )
    if request.method == "POST":
        plan = request.POST.get("plan")
        # تحقق ديناميكي من القيم الموجودة في الموديل
        valid_plans = dict(Subscription.PLAN_CHOICES).keys()

        if plan not in valid_plans:
            return redirect("upgrade_plan")
        subscription.plan = plan
        subscription.save()
        return redirect("add_product")
    context = {
        "plans": Subscription.PLAN_CHOICES,
        "current_plan": subscription.plan,
    }
    return render(request, "app/upgrade_plan.html", context)
#--------------------- / Plan --------------------------------


#--------------------- shop --------------------------------
# @login_required # shop list
def shop(request, username):
    
    shop_user  = get_object_or_404(User, username=username)
    products   = Product.objects.filter(user=shop_user)
    plan       = shop_user.subscription.plan
    max_products = shop_user.subscription.max_products()      

    context = {
        'shop_user': shop_user,
        'products': products,
        'plan': plan,
        'max_products': max_products
    }
    return render(request, 'app/shop.html', context)
#--------------------- / shop ------------------------------

#--------------------- Category --------------------------------
@login_required # add_category
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
   
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('store')
    else:
        form = CategoryForm()
    
    context = {'form': form, 'title': 'Add Category'}
    return render(request, 'app/category_form.html', context)

@login_required # update_category
@user_passes_test(lambda u: u.is_superuser)
def update_category(request, slug):
    
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('store')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'title': 'Edit Category', 'category': category}
    return render(request, 'app/category_form.html', context)

@login_required # delete_category
@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, slug):
    
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('store')
    
    context = {'category': category}
    return render(request, 'app/category_confirm_delete.html', context)
#--------------------- / Category ------------------------------

#--------------------- Product --------------------------------
@login_required # add_product
def add_product(request):
    """
    Add new product
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            # Save uploaded images
            images = request.FILES.getlist("images")
            for img in images:
                ProductImages.objects.create(product=product, image=img)

            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()

    return render(request, "app/product_form.html", {"form": form})

import json
@login_required # update_product
def update_product(request, slug):
    """
    Update existing product
    """
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # Save new uploaded images
            new_images = request.FILES.getlist("images")
            for img in new_images:
                ProductImages.objects.create(product=product, image=img)

           

            image_order = request.POST.get("image_order")

            if image_order:
                image_order = json.loads(image_order)

                for item in image_order:
                    img = ProductImages.objects.get(id=item["id"])
                    img.order = item["order"]
                    img.save()

            # Optional: handle image order here if sent via POST
            # Example: order = request.POST.getlist("image_order[]")
            # loop through order and update an order field in ProductImage

            return redirect(product.get_absolute_url())
    else:
        form = ProductForm(instance=product)
 
    context = {'form': form, 'title': 'Edit Product', 'product': product}
    return render(request, 'app/product_form.html', context)

@login_required # delete_product
def delete_product(request, slug):
 
    product = get_object_or_404(Product, slug=slug)
    
    # Check if the user is the owner of the product
    if product.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('shop')

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('store', request.user.username)
    
    context = {'product': product}
    return render(request, 'app/product_confirm_delete.html', context)

def product_detail(request, slug): # product_detail
   
    product = get_object_or_404(Product, slug=slug)
    # Get related products based on category
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(slug=slug)[:8]
    
    context = {
        'product': product,
        'related_products': related_products 
    }
    return render(request, 'app/product_detail.html', context)

@login_required # manage_product_images
def manage_product_images(request, slug):
   
    product = get_object_or_404(Product, slug=slug)

    # if product.user != request.user and not request.user.is_superuser:
    #     messages.error(request, 'You are not authorized to manage this product\'s images.')
    #     return redirect('product', slug=slug)

    images = product.images.all()
    form = ProductImageForm()
    context = {'form': form, 'product': product,  'images': images }
    return render(request, 'app/product_images.html', context)

@login_required # add_product_image
def add_product_image(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if product.user != request.user and not request.user.is_superuser:
        messages.error(request, 'Not authorized.')
        return redirect('product', slug=slug)

    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.product = product
            img.save()
            messages.success(request, 'Image added successfully!')
        else:
            messages.error(request, 'Failed to upload image. Please try again.')

    return redirect('manage_product_images', slug=slug)

@login_required # delete_product_image
@csrf_exempt
def delete_product_image(request, image_id):
    """
    Delete an image via AJAX
    """
    image = get_object_or_404(ProductImages, id=image_id)
    if request.method == "POST":
        image.delete()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)

def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('shop')
    
    context = {'category': category}
    return render(request, 'app/category_confirm_delete.html', context)
#--------------------- / Category --------------------------------
    return redirect('manage_product_images', slug=product.slug)
#--------------------- / Product --------------------------------

#--------------------- Wishlist --------------------------------
@login_required # wishlist_list
def wishlist_list(request):
 
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    
    context = {
        'products': products
    }
    return render(request, 'app/wishlist.html', context)

@login_required # add_to_wishlist
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')

@login_required # remove_from_wishlist
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')
#--------------------- / Wishlist --------------------------------


#---------------------  Brands --------------------------------
def brands(request): # brands list  
    brands = Brand.objects.filter(is_active=True)
    context = {'brands': brands}
    return render(request, 'app/brands.html', context)

@login_required 
@user_passes_test(lambda u: u.is_superuser) # add brand
def add_brand(request):
   
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully!')
            return redirect('brands')
    else:
        form = BrandForm()
    
    context = {'form': form, 'title': 'Add Brand'}
    return render(request, 'app/brand_form.html', context)

@login_required 
@user_passes_test(lambda u: u.is_superuser) # update brand
def update_brand(request, slug):
  
    brand = get_object_or_404(Brand, slug=slug)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully!')
            return redirect('brands')
    else:
        form = BrandForm(instance=brand)
    
    context = {'form': form, 'title': 'Edit Brand'}
    return render(request, 'app/brand_form.html', context)

@login_required 
@user_passes_test(lambda u: u.is_superuser) # delete brand
def delete_brand(request, slug):
    
    brand = get_object_or_404(Brand, slug=slug)
    
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand deleted successfully!')
        return redirect('brands')
    
    context = {'brand': brand}
    return render(request, 'app/brand_confirm_delete.html', context)
#---------------------  / Brans ------------------------------
