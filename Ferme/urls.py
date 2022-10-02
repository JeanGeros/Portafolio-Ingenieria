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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('pwa.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.Index, name="index"),
    path('ingreso_usuarios/', views.Ingreso, name="ingreso"),

    path('seleccion_registro/', views.Seleccion_registro, name="seleccion_registro"),
    path('registro_cliente/', views.Registro_clientes, name="registro_clientes"),

    path('clientes/ver_perfil/', views.Ver_perfil, name="ver_perfil"),
    path('clientes/editar_perfil/', views.Editar_perfil, name="editar_perfil"),
    path('clientes/revisar_compras/', views.Revisar_compras, name="revisar_compras"),

    path('registro_cliente_empresa/', views.Registro_clientes_empresa, name="registro_clientes_emp"),
    path('clientes/', views.Listar_clientes, name="listar_clientes"),
    path('clientes/agregar_cliente', views.Agregar_cliente, name="agregar_cliente"),
    path('clientes/ver_cliente', views.Ver_cliente, name="ver_cliente"),
    path('clientes/editar_cliente', views.Editar_cliente, name="editar_cliente"),
    
    path('productos/', views.Listar_productos, name="listar_productos"),
    path('productos/agregar_producto/', views.Agregar_productos, name="agregar_productos"),
    path('productos/ver_producto', views.Ver_producto, name="ver_productos"),
    path('productos/editar_producto', views.Editar_producto, name="editar_productos"),

    path('vendedores/', views.Listar_vendedores, name="listar_vendedores"),
    path('vendedores/agregar_vendedor', views.Agregar_vendedor, name="agregar_vendedor"),
    path('vendedores/ver_vendedor', views.Ver_vendedor, name="ver_vendedor"),
    path('vendedores/editar_vendedor', views.Editar_vendedor, name="editar_vendedor"),
    path('vendedores/listar_clientes_vendedor', views.Listar_clientes_vendedor, name="listar_clientes_vendedor"),
    path('vendedores/ver_cliente_vendedor', views.Ver_cliente_vendedor, name="ver_cliente_vendedor"),
    path('vendedores/agregar_cliente_vendedor', views.Agregar_cliente_vendedor, name="agregar_cliente_vendedor"),
    path('vendedores/editar_cliente_vendedor', views.Editar_cliente_vendedor, name="editar_cliente_vendedor"),

    path('proveedores/', views.Listar_proveedores, name="listar_proveedores"),
    path('proveedores/agregar_proveedor/', views.Agregar_proveedor, name="agregar_proveedor"),
    path('proveedores/ver_proveedor', views.Ver_proveedor, name="ver_proveedor"),
    path('proveedores/editar_proveedor', views.Editar_proveedor, name="editar_proveedor"),
    
    path('empleados/', views.Listar_empleados, name="listar_empleados"),
    path('empleados/agregar_empleado', views.Agregar_empleado, name="agregar_empleado"),
    path('empleados/ver_empleado', views.Ver_empleado, name="ver_empleado"),
    path('empleados/editar_empleado', views.Editar_empleado, name="editar_empleado"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)