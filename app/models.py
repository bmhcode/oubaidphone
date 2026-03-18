from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.utils.text import slugify
import uuid
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ValidationError

from django.utils.html import mark_safe
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta

from django_ckeditor_5.fields import CKEditor5Field

# cloudinary
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import MediaCloudinaryStorage
# / cloudinary

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

    
class Subscription(models.Model):

    PLAN_CHOICES = (
        ('FREE', 'Free'),
        ('PRO', 'Pro'),
        ('BUSINESS', 'Business'),
    )

    PLAN_LIMITS = {
        'FREE': 3,
        'PRO': 5,
        'BUSINESS': None,  # None = Unlimited
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='FREE')

    def max_products(self):
        return self.PLAN_LIMITS.get(self.plan)

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

class Store(models.Model):
    name    = models.CharField('name of store', max_length=255, blank=True, null=False, default="Store name")
    about_us = CKEditor5Field('Text', config_name='extends')
    address = models.CharField(max_length=255, blank=True, null=True, default="Store adress")
    phone  = models.CharField('Contact Phone',max_length=255, blank=True, null=True, default="Store phone")
    email  = models.EmailField('Email Address', max_length=255, default="store@mail.com")
    # logo   = models.ImageField(blank=True, default='', upload_to="store")
    # logo   = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)  # صورة المنتج على Cloudinary
    logo = CloudinaryField('logo', blank=True, null=True)
    
    # image1 = models.ImageField(blank=True, default='image1', upload_to="store")
    # image1 = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)  # صورة المنتج على Cloudinary
    image1 = CloudinaryField('image1', blank=True, null=True)
    title1 = models.CharField(max_length=50, blank=True, null=True, default="title1")
    subtitle1 = models.CharField(max_length=50, blank=True, null=True, default="subtitle1")
    description1 = CKEditor5Field('Text', config_name='extends')

    # image2 = models.ImageField(blank=True,default='image2', upload_to="store")
    # image2 = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)  # صورة المنتج على Cloudinary
    image2 = CloudinaryField('image2', blank=True, null=True)
    title2 = models.CharField(max_length=50, blank=True, null=True, default="title2")
    subtitle2 = models.CharField(max_length=50, blank=True, null=True, default="subtitle2")
    description2 = CKEditor5Field('Text', config_name='extends')

    # image3 = models.ImageField(blank=True, default='image3', upload_to="store")
    # image3 = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)  # صورة المنتج على Cloudinary
    image3 = CloudinaryField('image3', blank=True, null=True)
    title3 = models.CharField(max_length=50, blank=True, null=True, default="title3")
    subtitle3 = models.CharField(max_length=50, blank=True, null=True, default="subtitle3")
    description3 = CKEditor5Field('Text', config_name='extends')

    # web = models.URLField('Website Adress',null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def logoURL(self):
        try:
            url = self.logo.url
        except:
            url = ''
        return url
    
    @property
    def imageURL_1(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url
    
    @property
    def imageURL_2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    
    @property
    def imageURL_3(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url

# class StoreSection(models.Model):
#     store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="sections")
#     title = models.CharField(max_length=50)
#     subtitle = models.CharField(max_length=50)
#     description = CKEditor5Field('Text', config_name='extends')
#     image = CloudinaryField('image')

class Brand(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_("Name of brand"),
        db_index=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=160
    )

    image = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    start_date = models.DateTimeField(
        verbose_name=_("Start at"),
        default=timezone.now
    )

    end_date = models.DateTimeField(
        verbose_name=_("End at"),
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    # 🔹 slug auto-generate (clean + safe)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)

            # prevent duplicates
            slug = base_slug
            while Brand.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

            self.slug = slug

        super().save(*args, **kwargs)

    # 🔹 safe image URL
    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        return ""

    # 🔹 check if brand is currently active (based on date)
    @property
    def is_current(self):
        now = timezone.now()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date <= now

class Category(models.Model):
    name   = models.CharField(unique=True, max_length=100, verbose_name=_("Category")) #,default='name of the category', help_text='name of catygory')
    slug   = models.SlugField(blank=True,null=True, unique=True)
    # image = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)  # صورة المنتج على Cloudinary
    # image  = models.ImageField(upload_to='category',default='category.jpg')
    image = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural= 'Categories'
      
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)            
      
    def get_absolute_url(self):
        return reverse('index')
        # return 'https://www.google.fr'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    # def category_image(self):
    #     return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def category_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return "-"    

class Product(models.Model):
    user     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name     = models.CharField(unique=True, max_length=128, verbose_name =_('Name of product'))
    slug     = models.SlugField(unique=True)
    price    = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True,null=True)
    description = CKEditor5Field('Text', config_name='extends')

    # image    = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)  # صورة المنتج على Cloudinary
    image = CloudinaryField('image', blank=True, null=True)

    created  = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated  = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    is_active = models.BooleanField(default=False)

    # old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True,null=True, verbose_name =_('old price'))
    # is_featured = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.name}" # ({self.description[0:50]})"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = _("Product")
        # verbose_name_plural = _("Products")

    # class Meta:
    # indexes = [
    #     models.Index(fields=['slug']),
    #     models.Index(fields=['is_active']),
    # ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
            
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
        # return reverse('index')
        # return 'https://www.google.fr'

    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    # Adminلعرض صورة مصغرة في 
    def product_image(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % self.image.url)
        return "-"  

    @property
    def user_phone(self):
        if hasattr(self.user, 'profile'):
            return self.user.profile.phone
        return None

    def is_new(self):
        return self.created >= timezone.now() - timedelta(days=3)


    # @property
    # def time_since_created(self):
    #     delta = timezone.now() - self.created
    #     seconds = delta.total_seconds()
        
    #     if seconds < 60:
    #         return "Just now"
    #     elif seconds < 3600:
    #         return f"il ya {int(seconds // 60)} minutes ago"
    #     elif seconds < 86400:
    #         return f"il ya {int(seconds // 3600)} hours ago"
    #     elif seconds < 604800:
    #         return f"il ya {int(seconds // 86400)} days ago"
    #     else:
    #         return self.created.strftime("%d %b %Y")
    @property
    def is_new(self):
        """يرجع True إذا المنتج تم إنشاؤه منذ أقل من 7 أيام"""
        return timezone.now() - self.created <= timedelta(days=1)


    product_image.short_description = 'Image'
    # def get_precentage(self):
    #     new_price = (self.price / self.old_price) * 100
    #     return new_price

    @property
    def main_image(self):
        first = self.images.first()
        if first:
            return first.image.url
        return ""
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,related_name='images', verbose_name=_("Product images"))
    caption = models.CharField(max_length=128, blank=True, null=True)
    image   = CloudinaryField('image', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)  
    # models.py
    order = models.PositiveIntegerField(default=0) 
    # image   = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)  # صورة المنتج على Cloudinary
    # image       = models.ImageField(upload_to='product-images', default='product.jpg') #/%y/%m/%d')
   
    class Meta:
        verbose_name_plural = _("Product images") 
        ordering = ['order', 'created']

    def __str__(self):
        return f"Image of {self.product.name} - {self.id}"
      
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist for {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    image   = CloudinaryField('image', blank=True, null=True)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Vender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="venders")

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField(blank=True)

    # ✅ IMAGE
    # image = models.ImageField(upload_to="venders/", blank=True, null=True)
    image   = CloudinaryField('image', blank=True, null=True)
    # ✅ TRANSACTION RATIO (commission %)
    transaction_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage (%)")

    # ✅ PASSWORD (hashed)
    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_of_contract = models.DateTimeField(blank=True, null=True)
    end_of_contract = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def save(self, *args, **kwargs):
        # slug auto
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:6]

        # hash password if not hashed
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    # helper (optional)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ""

# =========================
# SALES MODEL
# =========================
class Sale(models.Model):
    vender = models.ForeignKey(Vender, on_delete=models.CASCADE, related_name="sales")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # ✅ TRANSACTION AMOUNT
    transaction_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    # ✅ TRANSACTION RATIO (commission %)
    transaction_ratio = models.DecimalField(max_digits=5,decimal_places=2,default=0.00,help_text="Percentage (%)")
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.vender.name}"

    def save(self, *args, **kwargs):
        # auto slug
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(uuid.uuid4())[:6]

        # calculate profit
        self.profit = self.transaction_amount * self.transaction_ratio/100

        super().save(*args, **kwargs)