from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from cart.models import Order, OrderItem, Payment,WishList,WishListItem
from .models import Category,Product,Product_Image
from django.views import View
# Create your views here.


class HomeView(View):
    def get(self, request):
        try:
            search = request.GET.get("q")
            products = Product.objects.filter(title__icontains=search)
            contex = {
                'products' : products,
            }
            return render(request, 'product/home.html', contex)
        except:
            products = Product.objects.all()
            contex = {
                'products' : products,
            }
            return render(request, 'product/home.html', contex)
    

class ProductView(View):
    def get(self, request,pk):
        product = get_object_or_404(Product, pk = pk)
        contex = {
            'product' : product,

        }
        return render(request, 'product/product_details.html',contex)

class CategoryView(View):
    def get(self, request,pk):
        products = Product.objects.filter(category__id = pk)
        category = get_object_or_404(Category, pk = pk)
        
        contex = {
            'products' : products,
            'category':category,

        }
        return render(request, 'product/category.html',contex)
    