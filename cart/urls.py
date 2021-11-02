from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name="cart"),
    path('update_item/', views.UpdateItemView.as_view(), name="update_item"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('wishlist_item/', views.WishListItemView.as_view(), name="wishlist_item"),
    path('chackout/', views.checkouts , name="chackout"),
    path('coupon/', views.coupon_check , name="coupon"),
]