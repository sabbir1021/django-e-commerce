from django.shortcuts import render,get_object_or_404
from .models import Order, OrderItem, Payment, WishList, WishListItem
from product.models import Product
from accounts.models import ShippingAddress
from django.views import View
from django.http import JsonResponse
import json
# Create your views here.

class CartView(View):
    def get(self, request):
        try:
            order = get_object_or_404(Order, user=request.user,confirm_order=False, complete_order=False)
            items = order.orderitem_set.all()
        except:
            order ={'get_item_total':0}
            items = []

        return render(request, "cart/cart.html",{'items':items,'order':order})


class UpdateItemView(View):
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        user = request.user
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(user=user,confirm_order=False, complete_order=False)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            orderitem.quantity = (orderitem.quantity +1)
        elif action == 'sub':
            orderitem.quantity = (orderitem.quantity -1)
        orderitem.save()
        if action == 'del':
            orderitem.delete()
        
        if orderitem.quantity <=0:
            orderitem.delete()
        return JsonResponse('item' , safe=False)

def wishlist(request):
    wishlist = get_object_or_404(WishList, user=request.user)
    wishitems = wishlist.wishlistitem_set.all()
    context = {
        'wishlist':wishlist,
        'wishitems':wishitems
    }
    return render(request, "cart/wishlist.html",context)


class WishListItemView(View):
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        user = request.user
        product = Product.objects.get(id=productId)
        print(productId)
        wishlist, created = WishList.objects.get_or_create(user=user)
        wishlistitem, created = WishListItem.objects.get_or_create(wishlist=wishlist, product=product)
        if action == "del":
            wishlistitem.delete()
        return JsonResponse('item' , safe=False)

def checkouts(request):
    shippings = ShippingAddress.objects.filter(user= request.user)
    context= {
        'shippings':shippings
    }
    return render(request, "cart/checkout.html",context)