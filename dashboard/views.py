from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views import View 
from cart.models import Order,OrderItem
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper

@superuser_required()
class StafAdminView(View):
    def get(self, request):
        orders_confirm = Order.objects.filter(confirm_order=True, complete_order = False)
        orders_complete = Order.objects.filter(confirm_order=True, complete_order = True).order_by('-id')
        context ={
            'orders_confirm':orders_confirm,
            'orders_complete':orders_complete
        }
        return render(request, "dashboard/staf_admin.html",context)

@superuser_required()
class OrderDetailsView(View):
    def get(self, request,*args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['id'])
        items = order.orderitem_set.all()
        payment = order.payment_set.all()
        context ={
            'order':order,
            'items':items,
            'payment':payment
        }
        return render(request, "dashboard/order_details.html",context)
    def post(self, request,*args, **kwargs):
        if request.method == 'POST':
            order_complete = request.POST.get("complete")
            if order_complete == 'yes':
                order = get_object_or_404(Order, pk=kwargs['id'])
                order.complete_order = True
                order.save()
                return redirect('dashboard:dashboards')