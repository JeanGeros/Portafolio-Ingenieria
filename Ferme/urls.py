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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.Index, name="index"),
    path('ingreso_usuarios/', views.Ingreso, name="ingreso"),

    path('registro_cliente/', views.Registro_clientes, name="registro_clientes"),
    path('clientes/', views.Listar_clientes, name="listar_clientes"),
    path('clientes/ver_cliente', views.Ver_cliente, name="ver_cliente"),
    path('clientes/editar_cliente', views.Editar_cliente, name="editar_cliente"),
    
    path('agregar-producto/', views.addProducts, name="agregar-producto"),
    path('listar-producto/', views.listar_productos, name="listar-producto"),
]
