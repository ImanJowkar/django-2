from django.shortcuts import render
from django.views import View

# Create your views here.

class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html')
    
    
    def post(self, request, *args, **kwargs):
        return render(request, 'home/index.html')