from django.contrib import admin

from .models import (
    Accionpagina, Boleta, Cliente, Comuna, Despacho, Detalleorden, Tipoproducto, Tiporubro,
    Direccion, Empleado, Empresa, Factura, Familiaproducto, Guiadespacho, Notacredito, Direccioncliente,
    Persona, Producto, Proveedor, Recepcion, Region, Rolusuario, Tipobarrio, Tipodocumento,Detalleventa, 
    Tipovivienda, Usuario, Venta, Estado, Estadoorden, Ordencompra, Productoproveedor, Bodega, Tipopago
)

admin.site.register(Accionpagina)
admin.site.register(Productoproveedor)
admin.site.register(Bodega)
admin.site.register(Boleta)
admin.site.register(Cliente)
admin.site.register(Comuna)
admin.site.register(Despacho)
admin.site.register(Detalleorden)
admin.site.register(Direccioncliente)
admin.site.register(Direccion)
admin.site.register(Empleado)
admin.site.register(Empresa)
admin.site.register(Estado)
admin.site.register(Estadoorden)
admin.site.register(Factura)
admin.site.register(Familiaproducto)
admin.site.register(Guiadespacho)
admin.site.register(Notacredito)
admin.site.register(Ordencompra)
admin.site.register(Persona)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Recepcion)
admin.site.register(Region)
admin.site.register(Rolusuario)
admin.site.register(Detalleventa)
admin.site.register(Tipobarrio)
admin.site.register(Tipodocumento)
admin.site.register(Tipoproducto)
admin.site.register(Tiporubro)
admin.site.register(Tipovivienda)
admin.site.register(Usuario)
admin.site.register(Venta)
admin.site.register(Tipopago)

