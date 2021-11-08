from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'dashboard'

urlpatterns = [
    path('', views.StafAdminView.as_view(), name="dashboards"),
    path('order_details/<int:id>', views.OrderDetailsView.as_view(), name="order_details"),
    path('pdf_create<int:id>', views.create_pdf, name="pdf_create"),
    
]