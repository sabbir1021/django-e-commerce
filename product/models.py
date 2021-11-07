from django.db import models
from django.db.models.fields.related import ForeignKey
from django.urls.base import reverse
from django.db.models.signals import pre_save
from utils.receivers import slugify_pre_save
from django.contrib.auth import get_user_model
User = get_user_model()
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime

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
    sort_description = RichTextField(blank=True, null=True)
    description = RichTextField()
    additional_information = RichTextField(blank=True, null=True)
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
    def all_reviews(self):
        all_reviews = self.reviews.all()
        return all_reviews

    @property
    def all_reviews_rating(self):
        all_reviews = self.reviews.all()
        if all_reviews:
            total = 0
            l = len(all_reviews)
            for rev in all_reviews:
                total = total + rev.rating
            avg = total/ l
            return (avg*20)
        else:
            return 0

    @property
    def new_price(self):
        try:
            dis = (self.discount.discount_percent * self.price) / 100
            total = self.price - dis
            return round(total, 2)
        except:
            return 0
    
    @property
    def timecheck(self):
        d1 = datetime.now()
        d2 = datetime(year = self.created_at.year , month= self.created_at.month , day = self.created_at.day, hour = self.created_at.hour , minute = self.created_at.minute)
        d = d1 - d2
        d_days = d.days
        return d_days

        
    
    
class Product_Image(models.Model):
    product = models.ForeignKey(Product,related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/')
    

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='reviews', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = '4. Product Review'

    def __str__(self):
        return str(self.user)

    @property
    def rating_convert(self):
        return (self.rating*20)

        
pre_save.connect(slugify_pre_save, sender=Category)
pre_save.connect(slugify_pre_save, sender=Product)