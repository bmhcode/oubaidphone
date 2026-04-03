from .views import _get_store
from .models import Category, Wishlist
from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}

def global_data(request):
    return {
        'store': _get_store(),
        'categories': Category.objects.filter(is_active=True)
    }


def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            count = wishlist.products.count()
        except Wishlist.DoesNotExist:
            count = 0
    return {'nbr_wishlist': count}

def user_has_shop(request):
    if request.user.is_authenticated:
        return {
            "has_shop": request.user.shops.exists(),
            "first_shop": request.user.shops.first(),
        }
    return {}