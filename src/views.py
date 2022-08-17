from django.shortcuts import render
from .forms import addproductsForm

def Index(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def addProducts(request):
    data = {
        'form': addproductsForm()
    }
    return render(request, 'SalesModule/addProducts.html', data)