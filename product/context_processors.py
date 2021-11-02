from django.shortcuts import get_object_or_404
from .models import Category
from cart.models import Order, WishList
def categories(request):
    all_cats = Category.objects.all()
    return {'all_categories': all_cats}

def order(request):
    try:
        order = get_object_or_404(Order, user=request.user, confirm_order=False,complete_order=False)
        items = order.orderitem_set.all()
    except:
        order ={'get_item_total':0}
        items = []
    return {'order': order,'items':items}

def wish(request):
    try:
        wishlist = get_object_or_404(WishList, user=request.user)
        wishitems = wishlist.wishlistitem_set.all()
    except:
        wishlist ={'get_item_total':0}
        wishitems = []
    return {'wishlist': wishlist,'wishitems':wishitems}