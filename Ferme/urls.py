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
from django.urls import path, include
from django.conf import settings
from src import views, static 

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('index/', views.Index, name="index"),
    path('ingreso_usuarios/', views.Ingreso, name="ingreso"),

    path('registro_cliente/', views.Registro_clientes, name="registro_clientes"),
    path('clientes/', views.Listar_clientes, name="listar_clientes"),
    path('clientes/ver_cliente', views.Ver_cliente, name="ver_cliente"),
    path('clientes/editar_cliente', views.Editar_cliente, name="editar_cliente"),
    
    path('productos/', views.Listar_productos, name="listar_productos"),
    path('productos/agregar_producto/', views.Agregar_productos, name="agregar_productos"),
    path('productos/ver_producto', views.Ver_producto, name="ver_productos"),
    path('productos/editar_producto', views.Editar_producto, name="editar_productos"),

    path('vendedores/', views.Listar_vendedor, name="listar_vendedores"),
    path('vendedores/agregar_vendedor', views.Agregar_vendedor, name="agregar_vendedor"),
    path('vendedores/ver_vendedor', views.Ver_vendedor, name="ver_vendedor"),
    path('vendedores/editar_vendedor', views.Editar_vendedor, name="editar_vendedor"),

    path('proveedores/', views.Listar_proveedores, name="listar_proveedores"),
    # path('productos/agregar_producto/', views.Agregar_productos, name="agregar_productos"),
    path('proveedores/ver_proveedor', views.Ver_proveedor, name="ver_proveedor"),
    # path('productos/editar_producto', views.Editar_producto, name="editar_productos"),

]
