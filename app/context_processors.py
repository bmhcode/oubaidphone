from .views import _get_mystore
from .models import Category, Wishlist

def global_data(request):
    return {
        'mystore': _get_mystore(),
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
