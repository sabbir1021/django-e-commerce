from django.shortcuts import render
from django.views.generic.base import View
from django.views import View 

# Create your views here.

class AboutView(View):
    def get(self, request):
        return render(request, "about/about.html")
