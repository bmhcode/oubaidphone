from django import forms
from .models import Store, Profile, Product, Brand, Category, ProductImages, Shop, Order, OrderItem, ShopReview, WorkingHours, ShopHoliday, ShopSocial, ShopValidation
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from django.forms import inlineformset_factory

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        # fields = '__all__'
        fields = [
            'user', 'name', 'phone', 'email', 'website', 'description', 'logo', 'cover', 
            'address', 'city', 'postal_code', 'country', 'latitude', 'longitude',
            'is_closed'
        ]
        labels = {
            'user': 'Owner',
        }
        widgets = {
            'user':        forms.Select(attrs={'class': 'form-control'}),
            'name':        forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone':       forms.TextInput(attrs={'class': 'form-control'}),
            'email':       forms.EmailInput(attrs={'class': 'form-control'}),
            'website':     forms.URLInput(attrs={'class': 'form-control'}), 
            'logo':        forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover':       forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'address':     forms.TextInput(attrs={'class': 'form-control'}),
            'city':        forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country':     forms.TextInput(attrs={'class': 'form-control'}),
            'latitude':    forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude':   forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            
            'is_closed':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # ✅ استقبل user
        super().__init__(*args, **kwargs)

        # ✅ إخفاء owner إذا ليس superuser
        if not user or not user.is_superuser:
            self.fields.pop('user', None)
    
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'name', 'about_us', 'address', 'phone', 'email', 'logo',
            'image1', 'title1', 'subtitle1', 'description1',
            'image2', 'title2', 'subtitle2', 'description2',
            'image3', 'title3', 'subtitle3', 'description3',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about_us': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            'image1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title1': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle1': forms.TextInput(attrs={'class': 'form-control'}),
            'description1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'image2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title2': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle2': forms.TextInput(attrs={'class': 'form-control'}),
            'description2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title3': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle3': forms.TextInput(attrs={'class': 'form-control'}),
            'description3': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}), #, 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), #, 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'caption'}),
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'image', 'start_date', 'end_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set input formats for datetime fields
        self.fields['start_date'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_date'].input_formats = ['%Y-%m-%dT%H:%M']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','image'] #,'first_name','last_name','is_vender']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(
                    attrs={
                        'class': 'd-none',
                        'accept': 'image/*',
                        'id': 'imageUpload'
                    }
                    )
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

#----------------------------- Order Form ----------------------------------

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'payment_method', 'notes']

        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter delivery address'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes'
            }),
        }

        labels = {
            'address': 'Delivery Address',
            'payment_method': 'Payment Method',
            'notes': 'Notes',
        }

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'address', 'payment_method', 'notes']

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter delivery address'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes'
            }),
        }

        labels = {
            'status': 'Order Status',
            'address': 'Delivery Address',
            'payment_method': 'Payment Method',
            'notes': 'Notes',
        }


#----------------------------- Order Item Form ----------------------------------
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['product', 'quantity', 'price', 'status', 'notes'],
    extra=0,
    can_delete=True
)

#----------------------------- Shop Review Form ----------------------------------
class ShopReviewForm(forms.ModelForm):
    class Meta:
        model = ShopReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(5, 0, -1)], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review here...'}),
        }

#----------------------------- Shop Social Form ----------------------------------
class ShopSocialForm(forms.ModelForm):
    class Meta:
        model = ShopSocial
        fields = ['facebook', 'instagram', 'twitter', 'tiktok', 'whatsapp', 'telegram', 'youtube']
        widgets = {
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/...'}),
            'tiktok': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://tiktok.com/@...'}),
            'whatsapp': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://wa.me/...'}),
            'telegram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://t.me/...'}),
            'youtube': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
        }

#----------------------------- Shop Validation Form ----------------------------------
class ShopValidationForm(forms.ModelForm):
    class Meta:
        model = ShopValidation
        fields = ['is_validated', 'observation', 'start_date', 'period']
        widgets = {
            'is_validated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'period': forms.Select(attrs={'class': 'form-select'}),
        }

#----------------------------- Inline Formsets ----------------------------------
WorkingHoursFormSet = inlineformset_factory(
    Shop, 
    WorkingHours, 
    fields=['day', 'open_time', 'close_time','is_closed'], 
    extra=7, 
    max_num=7,
    can_delete=False,
    widgets={
        'day': forms.HiddenInput(),
        'open_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        'close_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        'is_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
)

ShopHolidayFormSet = inlineformset_factory(
    Shop,
    ShopHoliday,
    fields=['name', 'date_begin', 'date_end'],
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'date_begin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    }
)
