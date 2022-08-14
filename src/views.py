from django.shortcuts import render


def Index(request):

    return render(request, 'index.html')
    return render(request, 'login.html')