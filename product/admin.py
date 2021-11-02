from django.contrib import admin
from .models import Category,Product,Product_Image, Discount , ProductReview
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 20

class ProductImageInline(admin.TabularInline):
    model = Product_Image
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['title']
    list_per_page = 20


admin.site.register(Discount)
admin.site.register(ProductReview)