from django import forms
from .models import Product, Brand, Category, ProductImages, Store
from ckeditor.widgets import CKEditorWidget

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'old_price', 'image', 'is_active', 'new_product', 'featured_product']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}), #, 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), #, 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Old Price (Optional)'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'new_product': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'featured_product': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'image', 'start', 'end', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set input formats for datetime fields
        self.fields['start'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end'].input_formats = ['%Y-%m-%dT%H:%M']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional caption'}),
        }

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
            'about_us': CKEditorWidget(),
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

