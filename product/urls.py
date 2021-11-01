from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'product'

urlpatterns = [

    path('', views.HomeView.as_view(), name="home"),
    path('details/<int:pk>', views.ProductView.as_view(), name="detalis"),
    path('category/<int:pk>', views.CategoryView.as_view(), name="category"),


]