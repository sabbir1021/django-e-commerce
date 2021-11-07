from django.shortcuts import render,get_object_or_404, redirect
from .models import Order, OrderItem, Payment, WishList, WishListItem, Coupon
from product.models import Product
from accounts.models import BillingAddress, ShippingAddress, User
from django.views import View 
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json


# Create your views here.

@method_decorator(login_required, name='dispatch')
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
            if product.quantity - orderitem.quantity > 0:
                orderitem.quantity = (orderitem.quantity +1)
            else:
                orderitem.quantity = (orderitem.quantity)
        elif action == 'sub':
            orderitem.quantity = (orderitem.quantity -1)
        orderitem.save()
        if action == 'del':
            orderitem.delete()
        
        if orderitem.quantity <=0:
            orderitem.delete()
        return JsonResponse('item' , safe=False)


@method_decorator(login_required, name='dispatch')
class WishLiatView(View):
    def get(self, request):
        wishlist = get_object_or_404(WishList, user=request.user)
        wishitems = wishlist.wishlistitem_set.all()
        context = {
            'wishlist':wishlist,
            'wishitems':wishitems
        }
        return render(request, "cart/wishlist.html",context)

    

    
@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class CheckOutView(View):
    def get(self,request):
        billings = BillingAddress.objects.filter(user=request.user)
        shippings = ShippingAddress.objects.filter(user= request.user)
        context= {
            'billings':billings,
            'shippings':shippings,
        
        }
        return render(request, "cart/checkout.html",context)
        
    def post(self,request):
        if request.method == 'POST':
            payment_method = request.POST.get("payment")
            t_id = request.POST.get("t_id")
            order = get_object_or_404(Order, user=request.user, confirm_order=False,complete_order=False)
            items = order.orderitem_set.all()
            for item in items:
                item.product.quantity = item.product.quantity - item.quantity
                if item.product.quantity == 0:
                    item.product.available = False
                    item.product.save()
                item.product.save()
            if payment_method == "bkash" and t_id:
                payment, created = Payment.objects.get_or_create(order=order,name=payment_method, trans_id=t_id)
            else:
                payment, created = Payment.objects.get_or_create(order=order,name=payment_method)
            
            order.billing_address = get_object_or_404(BillingAddress, id=request.POST.get("billing"))
            order.shipping_address = get_object_or_404(ShippingAddress, id=request.POST.get("shipping"))
            order.confirm_order = True
            order.save()
            return redirect('product:home')
  
        
@method_decorator(login_required, name='dispatch')
class CouponCheckView(View):
    def post(self,request):
        if request.method == 'POST':
            coupon_name = request.POST.get("coupon")
            try:
                if get_object_or_404(Coupon, coupon=coupon_name):
                    print(coupon_name)
                    order = get_object_or_404(Order, user=request.user, confirm_order=False,complete_order=False)
                    order.coupon_discount = get_object_or_404(Coupon, coupon=coupon_name)
                    order.save()
                    return redirect('cart:chackout')
            except:
                return redirect('cart:chackout')