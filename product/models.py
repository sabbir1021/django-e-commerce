from django.db import models
from django.urls.base import reverse
from django.db.models.signals import pre_save
from utils.receivers import slugify_pre_save

from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Category(MPTTModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True,blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name = 'Category'
            verbose_name_plural = '1. Categories'
    
    def __str__(self):
        return self.title


class Discount(models.Model):
    name  = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Discounts'
        verbose_name_plural = '2. Discounts'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug     = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField()
    price =  models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = '3. Products'

    def get_absolute_url(self):
        return reverse("product:detalis", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    
    @property
    def all_image(self):
        all_image = self.images.all()
        return all_image

    @property
    def new_price(self):
        dis = (self.discount.discount_percent * self.price) / 100
        total = self.price - dis
        return total
    
    
class Product_Image(models.Model):
    product = models.ForeignKey(Product,related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/')
    





pre_save.connect(slugify_pre_save, sender=Category)
pre_save.connect(slugify_pre_save, sender=Product)