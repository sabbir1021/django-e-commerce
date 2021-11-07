from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from cart.models import Order, OrderItem, Payment,WishList,WishListItem
import product
from .models import Category,Product,Product_Image
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


class HomeView(View):
    def get(self, request):
        try:
            search = request.GET.get("q")
            products = Product.objects.filter(title__icontains=search )
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
        related_products = Product.objects.filter(category=product.category).exclude(pk=pk)
        contex = {
            'product' : product,
            'related_products':related_products,

        }
        return render(request, 'product/product_details.html',contex)

class CategoryView(View):
    def get(self, request,pk):
        products = Product.objects.filter(category__in = Category.objects.get(pk=pk).get_descendants(include_self=True))
        paginator = Paginator(products, 3) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        categorys = Category.objects.get(pk=pk).get_descendants()
        categorys_asn = Category.objects.get(pk=pk).get_ancestors()
        category = get_object_or_404(Category, pk = pk)

        contex = {
            'products' : page_obj,
            'category':category,
            'categorys':categorys,
            'categorys_asn':categorys_asn,
            


        }
        return render(request, 'product/category.html',contex)
    