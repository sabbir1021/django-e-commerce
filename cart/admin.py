from django.contrib import admin
from .models import Order, OrderItem , Payment, WishList , WishListItem, Coupon


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(WishList)
admin.site.register(WishListItem)
admin.site.register(Coupon)
