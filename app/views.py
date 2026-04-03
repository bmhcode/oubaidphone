from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.contrib.auth.forms import UserCreationForm
from .forms import OrderUpdateForm, OrderItemFormSet

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.models import User
from .models import Store, Shop, Category, Product, ProductImages, Subscription, Brand, Wishlist, Profile, Order, OrderItem, OrderItemHistory, OrderHistory, ShopReview, WorkingHours, ShopHoliday, ShopSocial, ShopValidation
from django.db.models import Q, Count, Sum, Avg, Value, FloatField
from django.db.models.functions import Coalesce

from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    StoreForm, ProductForm, BrandForm, CategoryForm, ProductImageForm, 
    CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, ShopForm, 
    OrderForm, OrderUpdateForm, OrderItemForm, ShopReviewForm,
    ShopSocialForm, ShopValidationForm, WorkingHoursFormSet, ShopHolidayFormSet
)


def index(request): # index page
  
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
    paginator = Paginator(products, 8)
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

def list_products(request): # products list

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
    # / pagination

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
   
    return render(request, 'app/list_products.html', context)

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
def update_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('index')

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'user': user,
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

#---------------------  Shop --------------------------------

def list_shops(request): # list shops

    shops = Shop.objects.all() #.order_by('-created_at')  # مهم

    shops = shops.annotate(
        avg_rating=Coalesce(
            Avg('reviews__rating'),
            Value(0),
            output_field=FloatField()
        ),
        total_reviews=Count('reviews'),
        products_count=Count('products', distinct=True)
    ).order_by('-avg_rating')
    total_shops = shops.count()

    # shops = Shop.objects.select_related('social', 'validation')\
    #     .prefetch_related('working_hours', 'holidays')

    search = request.GET.get('search', '')
    if search:
        shops = shops.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(address__icontains=search) |
            Q(description__icontains=search)
        )

    paginator = Paginator(shops, 5)
    page_number = request.GET.get('page')
    shops_page = paginator.get_page(page_number)
    
    context = {
        'shops': shops_page,
        'search': search,
        'total_shops': total_shops,
    }

    return render(request, 'app/list_shops.html', context)  

def shop(request, shop_slug): # shop
    shop = get_object_or_404(Shop, slug=shop_slug)
    products = Product.objects.filter(shop=shop, is_active=True)
 
    # reviews
    reviews = shop.reviews.all().order_by('-created_at')
    
    # Process review submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = ShopReviewForm(request.POST)
        if form.is_valid():
            # Check if user already reviewed
            if not ShopReview.objects.filter(shop=shop, user=request.user).exists():
                review = form.save(commit=False)
                review.shop = shop
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted successfully!')
            else:
                messages.error(request, 'You have already reviewed this shop.')
            return redirect('shop', shop_slug=shop.slug)
    else:
        form = ShopReviewForm()

    # pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    product_pages = paginator.get_page(page_number)
    nums = "a" * product_pages.paginator.num_pages

    context = {
        'shop': shop,
        'products': product_pages,
        'nums': nums,
        'reviews': reviews,
        'review_form': form,
    }
    return render(request, 'app/shop.html', context)

@login_required # create shop
def create_shop(request):

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        social_form = ShopSocialForm(request.POST)
        hours_formset = WorkingHoursFormSet(request.POST)
        holiday_formset = ShopHolidayFormSet(request.POST)
        
    has_errors = (
        form.errors or
        social_form.errors or
        hours_formset.total_error_count() or
        holiday_formset.total_error_count() or
        (validation_form.errors if validation_form else False)
    )

    if form.is_valid() and social_form.is_valid() and hours_formset.is_valid() and holiday_formset.is_valid():
        shop = form.save(commit=False)
        if not request.user.is_superuser:
            shop.user = request.user
        shop.save()
            
        # Save Social
        social = social_form.save(commit=False)
        social.shop = shop
        social.save()
            
        # Save Working Hours
        hours_formset.instance = shop
        hours_formset.save()
            
        # Save Holidays
        holiday_formset.instance = shop
        holiday_formset.save()
            
        # Initialize Validation (for superuser to review)
        ShopValidation.objects.create(shop=shop)
            
        messages.success(request, 'Shop created successfully!')
        return redirect('list_shops')
    else:
        form = ShopForm()
        social_form = ShopSocialForm()
        # Initialize working hours with all 7 days
        initial_hours = [{'day': i, 'open_time': '09:00', 'close_time': '18:00'} for i in range(7)]
        hours_formset = WorkingHoursFormSet(initial=initial_hours)
        holiday_formset = ShopHolidayFormSet()

         
    # exclude_fields = [
    #         'logo', 'cover', 'address', 'city',
    #         'postal_code', 'country', 'latitude',
    #         'longitude', 'is_closed', 'is_active'
    #     ]  



    context = {
        'form': form, 
        'social_form': social_form,
        'hours_formset': hours_formset,
        'holiday_formset': holiday_formset,
        'has_errors': has_errors,
        'title': 'Create Shop',
        # 'exclude_fields': exclude_fields,   
    }
    return render(request, 'app/shop_form.html', context)

@login_required # update_shop
def update_shop(request, slug):
    shop_instance = get_object_or_404(Shop, slug=slug)
    
    if shop_instance.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to edit this shop.')
        return redirect('list_shops')
        
    social_instance, _ = ShopSocial.objects.get_or_create(shop=shop_instance)
    validation_instance, _ = ShopValidation.objects.get_or_create(shop=shop_instance)
    
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop_instance)
        social_form = ShopSocialForm(request.POST, instance=social_instance)
        hours_formset = WorkingHoursFormSet(request.POST, instance=shop_instance)
        holiday_formset = ShopHolidayFormSet(request.POST, instance=shop_instance)
        
        # Superuser only validation form
        validation_form = None
        if request.user.is_superuser:
            validation_form = ShopValidationForm(request.POST, instance=validation_instance)
            
        if form.is_valid() and social_form.is_valid() and hours_formset.is_valid() and holiday_formset.is_valid():
            if validation_form and not validation_form.is_valid():
                pass # fall through to render with errors
            else:
                shop = form.save(commit=False)
                if not request.user.is_superuser:
                    shop.user = request.user
                shop.save()
                social_form.save()
                hours_formset.save()
                holiday_formset.save()
                if validation_form:
                    validation_form.save()
                
                messages.success(request, 'Shop updated successfully!')
                return redirect('list_shops')
    else:
        form = ShopForm(instance=shop_instance)
        social_form = ShopSocialForm(instance=social_instance)
        hours_formset = WorkingHoursFormSet(instance=shop_instance)
        holiday_formset = ShopHolidayFormSet(instance=shop_instance)
        validation_form = ShopValidationForm(instance=validation_instance) if request.user.is_superuser else None
        
        # If no working hours exist (for old shops), provide initial data
        if not shop_instance.working_hours.exists():
            initial_hours = [{'day': i, 'open_time': '09:00', 'close_time': '18:00'} for i in range(7)]
            hours_formset = WorkingHoursFormSet(instance=shop_instance, initial=initial_hours)
        
    context = {
        'form': form,
        'social_form': social_form,
        'hours_formset': hours_formset,
        'holiday_formset': holiday_formset,
        'validation_form': validation_form,
        'title': 'Update Shop',
        'shop': shop_instance
    }
    return render(request, 'app/shop_form.html', context)

@login_required # delete_shop
def delete_shop(request, slug):
    shop_instance = get_object_or_404(Shop, slug=slug)
    
    # Check permission
    if shop_instance.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this shop.')
        return redirect('shop', username=shop_instance.user.username)
        
    if request.method == 'POST':
        shop_instance.delete()
        messages.success(request, 'Shop deleted successfully!')
        # return redirect('index')
        return redirect('list_shops')
        
    context = {'shop': shop_instance}
    return render(request, 'app/shop_confirm_delete.html', context)
#--------------------- / Shop --------------------------------

#--------------------- Category --------------------------------

def list_categories(request): # list_categories
    categories = Category.objects.all().annotate(
        total_products=Count('products', distinct=True)
    ).order_by('name')

    search = request.GET.get('search', '')
    if search:
        categories = categories.filter(name__icontains=search)

    paginator = Paginator(categories, 20)
    page_number = request.GET.get('page')
    categories_page = paginator.get_page(page_number)

    context = {
        'categories': categories_page,
        'search': search,
        'total': Category.objects.count(),
    }
    return render(request, 'app/list_categories.html', context)


@login_required # add_category
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
   
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('list_categories')
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
            return redirect('list_categories')
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
        return redirect('list_categories')
    
    context = {'category': category}
    return render(request, 'app/category_confirm_delete.html', context)
#--------------------- / Category ------------------------------


#--------------------- Product --------------------------------

@login_required # add_product
def add_product(request, shop_slug):
    """
    Add new product
    """
    shop = get_object_or_404(Shop, slug=shop_slug)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()

            # Save uploaded images
            images = request.FILES.getlist("images")
            for img in images:
                ProductImages.objects.create(product=product, image=img)
            return redirect('shop', shop.slug)
            # return redirect(product.get_absolute_url())
    else:
        form = ProductForm()

    context = {'title': 'Add Product', 'shop': shop, 'form': form, }
    return render(request, "app/product_form.html", context)

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
 
    context = {'title': 'Edit Product', 'shop': product.shop, 'form': form,  'product': product}
    return render(request, 'app/product_form.html', context)

@login_required # delete_product
def delete_product(request, slug):
 
    product = get_object_or_404(Product, slug=slug)
    
    # Check if the user is the owner of the product
    if product.shop.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('shop')

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('shop', product.shop.slug)
    
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

    # return redirect('manage_product_images', slug=product.slug)
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

# ============================ / Brans =========================

@login_required
@user_passes_test(lambda u: u.is_superuser) # brand list
def brand_list(request): 
    """List all registered brands - superuser only."""
    brand_list = Brand.objects.all().order_by('-start_date')

    search = request.GET.get('search', '')
    if search:
        brand_list = brand_list.filter(name__icontains=search) 

    paginator = Paginator(brand_list, 10)
    page_number = request.GET.get('page')
    brands_page = paginator.get_page(page_number)

    context = {
        'brand_list': brands_page,
        'search': search,
        'total': Brand.objects.count(),
    }
    return render(request, 'app/brand_list.html', context)

@login_required 
@user_passes_test(lambda u: u.is_superuser) # add brand
def add_brand(request):
   
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully!')
            return redirect('brand_list')
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
            return redirect('brand_list')
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
        return redirect('brand_list')
    
    context = {'brand': brand}
    return render(request, 'app/brand_confirm_delete.html', context)

# ============================ / Brans =========================

# ============================  Members =========================

# @login_required
@user_passes_test(lambda u: u.is_superuser) # list members
def list_members(request):
    """List all registered users - superuser only."""
    # members = User.objects.all().select_related('profile', 'subscription').order_by('-date_joined')

    members = User.objects.all().select_related('profile', 'subscription') \
                .annotate(total_products=Count('shops__products', distinct=True)) \
                .order_by('-date_joined')

    search = request.GET.get('search', '')
    if search:
        members = members.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    paginator = Paginator(members, 20)
    page_number = request.GET.get('page')
    members_page = paginator.get_page(page_number)

    context = {
        'members': members_page,
        'search': search,
        'total': User.objects.count(),
    }
    return render(request, 'app/list_members.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser) # Add user
def add_user(request):
    """List all registered users - superuser only."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_members')
    else:
        form = CustomUserCreationForm()
    
    context = {
            'form': form
    }
    return render(request, 'registration/add_user.html', context)

# ============================ / Members =========================

# ============================ Cart ==============================

from .cart import Cart

@login_required # cart add
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = request.POST.get('quantity', 1)
    
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    cart.add(product=product, quantity=quantity)
    messages.success(request, f"{product.name} added to your cart.")
    
    # Redirect back to where the user came from or cart detail
    next_url = request.META.get('HTTP_REFERER', 'cart_detail')
    return redirect(next_url)

@login_required # cart remove
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"{product.name} removed from your cart.")
    return redirect('cart_detail')

@login_required # cart detail
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'app/cart.html', {'cart': cart})

def cart_update(request, product_id, action): # Cart update
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if action == 'increase':
        cart.add(product=product, quantity=1, update_quantity=False)

    elif action == 'decrease':
        cart.add(product=product, quantity=-1, update_quantity=False)

    return redirect('cart_detail')

# ============================ / Cart ==============================

# ============================ Orders ==============================

@login_required # order create
def order_create(request):

    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Please add items to order.")
        return redirect('index')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order    = order,
                    product  = item['product'],
                    price    = item['price'],
                    quantity = item['quantity']
                    # status   = item['status']
                    # notes     = item['notes']
                )
            
            cart.clear()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    
    return render(request, 'app/order_form.html', {'form': form, 'cart': cart})
def orders_list(request, userid = None):  # orders list (All / User)
    # orders = Order.objects.all().order_by('-created_at')
    if userid:
        orders = Order.objects.filter(user_id=userid).select_related('user') \
                      .prefetch_related('items', 'items__product', 'history').order_by('-created_at')
    else:    
        orders = Order.objects.select_related('user') \
                      .prefetch_related('items', 'items__product', 'history').order_by('-created_at')

    search = request.GET.get('search', '')
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(status__icontains=search) |
            Q(user__username__icontains=search)
        )
     # pagination
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    order_pages = paginator.get_page(page_number)
    # nums = "a" * order_pages.paginator.num_pages
    # / pagination

    return render(request, 'app/order_list.html', {
        'search': search,
        'orders': order_pages,
        'order_pages': order_pages,
        # 'nums': nums,
        'status_choices': Order.STATUS_CHOICES,  # <--- مهم
    })

@login_required # orders items list (all / shop)
def orders_items_list(request, shop_slug = None): 

    if shop_slug:
        shop  = get_object_or_404(Shop, slug=shop_slug)
        items = OrderItem.objects.filter(product__shop=shop).select_related('order', 'product').order_by('-order_id')
    else:
        shop  = "All Shops" #None
        items = OrderItem.objects.all().order_by('-order_id')

    # ---------- pagination
    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    item_pages = paginator.get_page(page_number)
    nums = "a" * item_pages.paginator.num_pages
    # ---------- / pagination

    return render(request, 'app/orders_items_list.html', {
        'shop' : shop,
        
        'items': item_pages,
        'item_pages':item_pages,
        'nums': nums,
  'status_choices': OrderItem.STATUS_CHOICES,  # ← الحل هنا
        })







@login_required # order detail 
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk) #, user=request.user)
    return render(request, 'app/order_detail.html', {'order': order})

@login_required # order update 
def order_update0(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user and not request.user.is_superuser:
        messages.error(request, "You cannot edit this order")
        return redirect('order_list_all')

    if request.method == 'POST':
        old_status = order.status
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            if order.status != old_status:
                OrderHistory.objects.create(
                    order=order,
                    old_status=old_status,
                    new_status=order.status,
                    changed_by=request.user if request.user.is_authenticated else None
                )
                order.propagate_status_to_items(user=request.user if request.user.is_authenticated else None)

            return redirect('order_detail', pk=pk)
    else:
        form = OrderUpdateForm(instance=order)
    return render(request, 'app/order_update.html', {'form': form, 'order': order})

@login_required # order update 
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Permission check
    if order.user != request.user and not request.user.is_superuser:
        messages.error(request, "You cannot edit this order")
        return redirect('order_list_all')

    old_status = order.status

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)

        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.save()

            # Update totals and status
            order.update_total_price()
            order.update_status_from_items()

            # Save history if status changed
            if order.status != old_status:
                OrderHistory.objects.create(
                    order=order,
                    old_status=old_status,
                    new_status=order.status,
                    changed_by=request.user if request.user.is_authenticated else None
                )

            messages.success(request, "Order updated successfully")
            return redirect('order_detail', pk=order.pk)

    else:
        form = OrderUpdateForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'app/order_update.html', {
        'form': form,
        'formset': formset,
        'order': order
    })

@login_required # order delete 
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk) #, user=request.user)
    if order.user != request.user and not request.user.is_superuser:
        messages.error(request, "You cannot delete this order")
        return redirect('order_list_all')

    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted")
        return redirect('order_list_all')
    return render(request, 'app/order_confirm_delete.html', {'order': order})








@login_required # order item status
def order_item_status(request, pk, status):
    item = get_object_or_404(OrderItem, pk=pk)

    # تحقق أن الحالة صالحة
    valid_statuses = [s[0] for s in OrderItem.STATUS_CHOICES]
    if status in valid_statuses:
        old = item.status
        item.status = status
        item.save(update_fields=['status'])

        # حفظ التاريخ
        OrderItemHistory.objects.create(
            order_item=item,
            old_status=old,
            new_status=status,
            changed_by=request.user if request.user.is_authenticated else None
        )

        # تحديث حالة الطلب
        item.order.update_status_from_items()

    if request.user.is_superuser:
        return redirect('orders_items_list')   # مهم لإعادة تحميل الصفحة
    return redirect('orders_items_list_shop', item.product.shop.slug) # مهم لإعادة تحميل الصفحة    

@login_required # order status
def order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)

    valid_statuses = [s[0] for s in Order.STATUS_CHOICES]

    if status in valid_statuses:
        old = order.status
        order.status = status
        order.save(update_fields=['status'])

        OrderHistory.objects.create(
            order=order,
            old_status=old,
            new_status=status,
            changed_by=request.user if request.user.is_authenticated else None
        )
        
        order.propagate_status_to_items(user=request.user if request.user.is_authenticated else None)

    return redirect('order_list_all')


# ============================ / Orders ==============================
