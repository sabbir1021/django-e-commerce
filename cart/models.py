from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirm_order = models.BooleanField()
    complete_order = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name = 'Orders'
            verbose_name_plural = '1. Orders'

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        return sum(i.get_total for i in items)
    
    @property
    def get_item_total(self):
        items = self.orderitem_set.all()
        total = 0
        for i in items:
            quantity = i.quantity
            total = total + quantity
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
            verbose_name = 'OrderItems'
            verbose_name_plural = '2. OrderItems'

    def __str__(self):
        return str(self.order)
    
    @property
    def get_total(self):
        return self.product.price * self.quantity



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    trans_id = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name = 'Payments'
            verbose_name_plural = '3. Payments'

    def __str__(self):
        return self.name

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name = 'WishLists'
            verbose_name_plural = '4. WishLists'

    def __str__(self):
        return str(self.id)

    @property
    def get_item_total(self):
        items = self.wishlistitem_set.all()
        return len(items)

class WishListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)

    class Meta:
            verbose_name = 'WishListItems'
            verbose_name_plural = '5. WishListItems'

    def __str__(self):
        return str(self.wishlist)