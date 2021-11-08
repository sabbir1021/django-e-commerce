from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views import View 
from cart.models import Order,OrderItem
from django.contrib.auth.mixins import UserPassesTestMixin
#pdf generate
# import io
# from django.http import FileResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
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


def create_pdf(request,id):
    order = get_object_or_404(Order, pk=id)
    items = order.orderitem_set.all()
    payment = order.payment_set.all()
    template_path = 'dashboard/order_details_pdf.html'
    context = {'order': order , 'items':items, 'payment':payment }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_details_report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response