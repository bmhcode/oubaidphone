from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.utils.text import slugify
from django.utils.html import mark_safe
# from ckeditor.fields import RichTextField
import django.utils.timezone

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)
    
class Store(models.Model):
    name    = models.CharField('name of store', max_length=255, blank=True, null=False, default="Store name")
    about_us = models.TextField(null=True, blank=True, default="About Us")
    address = models.CharField(max_length=255, blank=True, null=True, default="Store adress")
    phone  = models.CharField('Contact Phone',max_length=255, blank=True, null=True, default="Store phone")
    email  = models.EmailField('Email Address', max_length=255, default="yourmail@gmail.com")
    logo   = models.ImageField(blank=True, default='', upload_to="store")
    
    image1 = models.ImageField(blank=True, default='image1', upload_to="store")
    title1 = models.CharField(max_length=50, blank=True, null=True, default="title1")
    subtitle1 = models.CharField(max_length=50, blank=True, null=True, default="subtitle1")
    description1 = models.TextField(null=True, blank=True, default="description1")

    image2 = models.ImageField(blank=True,default='image2', upload_to="store")
    title2 = models.CharField(max_length=50, blank=True, null=True, default="title2")
    subtitle2 = models.CharField(max_length=50, blank=True, null=True, default="subtitle2")
    description2 = models.TextField(null=True, blank=True, default="description2")

    image3 = models.ImageField(blank=True, default='image3', upload_to="store")
    title3 = models.CharField(max_length=50, blank=True, null=True, default="title3")
    subtitle3 = models.CharField(max_length=50, blank=True, null=True, default="subtitle3")
    description3 = models.TextField(null=True, blank=True, default="description3")


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

class Brand(models.Model):
    name  = models.CharField(max_length=128, verbose_name =_('Name of product'))
    slug  = models.SlugField(blank=True,null=True)
    image = models.ImageField(default='', upload_to='product/', blank=True, verbose_name=_('Image'))
    start = models.DateTimeField(verbose_name=_('Start at'))
    end   = models.DateTimeField(verbose_name=_('End at'))
    show  = models.BooleanField(default=False)
   
    def __str__(self):
        return  f"{self.name}" 
    
    class Meta:
        ordering = ['-start'] #, '-created']
            
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)
         
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Category(models.Model):
    name   = models.CharField(max_length=100, verbose_name=_("Category")) #,default='name of the category', help_text='name of catygory')
    slug   = models.SlugField(blank=True,null=True)
    image  = models.ImageField(upload_to='category',default='category.jpg')
    show   = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural= 'Categories'
      
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)            
      
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
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name =_('Name of product'))
    slug = models.SlugField(blank=True,null=True)
    description = models.TextField(null=True,blank=True, default='This is the product', verbose_name =_('informations about product')) #description = RichTextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField('discount', max_digits=12, decimal_places=2, default=0, blank=True,null=True)
    image   = models.ImageField(upload_to=user_directory_path, default='product.jpg') #upload_to='product',
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    show    = models.BooleanField(default=False)
    new     = models.BooleanField(default=False)
    featured_product = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.name}" # ({self.description[0:50]})"
    
    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = _("Product")
        # verbose_name_plural = _("Products")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
            
    def get_absolute_url(self):
        return reverse("product_detail",kwargs={"slug":self.slug})
        # return reverse('index')
        # return 'https://www.google.fr'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        # return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name=_("Product"))
    image       = models.ImageField(upload_to='product-images', default='product.jpg') #/%y/%m/%d')
    description = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name_plural = _("Product Images") 
      
