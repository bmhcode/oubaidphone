from .models import Wishlist

def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            count = wishlist.products.count()
        except Wishlist.DoesNotExist:
            count = 0
    return {'nbr_wishlist': count}
