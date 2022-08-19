"""Ferme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from src import views, static
from src.views import Index, Login, Registro_clientes ,addProducts
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.Index, name="index"),
     path('registro_cliente/', views.Registro_clientes, name="registro_clientes"),
    path('login/', views.Login, name="login"),
    path('agregar-producto/', views.addProducts, name="agregar-producto"),
]
