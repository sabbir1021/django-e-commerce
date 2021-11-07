from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'about'

urlpatterns = [
    path('', views.AboutView.as_view(), name="about"),
    
]