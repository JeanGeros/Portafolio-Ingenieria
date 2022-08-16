from django.shortcuts import render


def Index(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def SalesModule(request):
    return render(request, 'Cruds/salesModule.html')