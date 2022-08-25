from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from src.forms import (
    FormClienteNormal1, FormClienteNormal2, FormClienteNormal3, addproductsForm
)
from .models import (
    Persona, Direccion, Usuario, Cliente, Estado, Comuna, Tipobarrio, Tipovivienda, Rolusuario, 
    Proveedor, Tipoproducto, Producto, Familiaproducto
)

def Index(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def addProducts(request):
    form = addproductsForm()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        stockcritico = request.POST.get('stockcritico')
        fechavencimiento = request.POST.get('fechavencimiento')
        imagen = request.POST.get('imagen')
        proveedorid = request.POST.get('proveedorid')
        tipoproductoid = request.POST.get('tipoproductoid')
        familiaproid = request.POST.get('familiaproid')
        estadoid = request.POST.get('estadoid')

        proveedor = Proveedor.objects.get(proveedorid=proveedorid)
        tipo_producto = Tipoproducto.objects.get(tipoproductoid=tipoproductoid)
        familia_producto = Familiaproducto.objects.get(familiaproid=familiaproid)
        Estado_producto = Estado.objects.get(estadoid=estadoid)
        product = Producto.objects.create(
           nombre = nombre.strip(),
           precio = precio.strip(),
           stock = stock.strip(),
           stockcritico = stockcritico.strip(),
           fechavencimiento = fechavencimiento,
           codigo = 1234,
           imagen = imagen,
           proveedorid = proveedor,
           tipoproductoid = tipo_producto,
           familiaproid = familia_producto,
           estadoid = Estado_producto
        )
        product.save()
        
        if product is not None:
            product.save()
            messages.warning(request, 'Producto creado correctamente')
            return redirect('listar-producto')
        else:
            messages.warning(request, 'No se pudo crear el Producto')
    context = {
    'form': form,
    }
    return render(request, 'Modulo_productos/addProducts.html', context)

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'Modulo_productos/listarProductos.html', {'productos':productos})


def Registro_clientes(request):
    form1 = FormClienteNormal1()
    form2 = FormClienteNormal2()
    form3 = FormClienteNormal3()
    form4 = FormClienteNormal4()

    if request.method == 'POST':
        

        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellidopaterno')
        apellido_materno = request.POST.get('apellidomaterno')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        calle = request.POST.get('calle')
        numero = request.POST.get('numero')
        comuna_id = request.POST.get('comunaid')
        tipo_vivienda_id = request.POST.get('tipoviviendaid')
        tipo_barrio_id = request.POST.get('tipobarrioid')
        nombre_sector = request.POST.get('nombresector')
        contraseña = request.POST.get('password')
        print(contraseña)
        confirm_contraseña = request.POST.get('confirm_password')
        print(confirm_contraseña)

        if contraseña == confirm_contraseña:
        
            # Estado activo = 1 e inactivo = 2 
            Persona.objects.create(
                runcuerpo = run_cuerpo,
                dv = dv,
                apellidopaterno = apellido_paterno,
                apellidomaterno = apellido_materno,
                nombres = nombres,
                telefono = telefono,
                estadoid = Estado.objects.get(descripcion="Activo")
            )

            Direccion.objects.create(
                calle = calle,
                numero = numero,
                comunaid = Comuna.objects.get(comunaid=comuna_id),
                tipoviviendaid = Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id),
                tipobarrioid = Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id),
                nombresector = nombre_sector
            )

            Cliente.objects.create(
                direccionid = Direccion.objects.get(calle=calle, numero=numero),
                personaid = Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                estadoid = Estado.objects.get(descripcion="Activo")
            )

            Usuario.objects.create(
                email = email,
                password = contraseña,
                personaid = Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                rolid = Rolusuario.objects.get(descripcion="Cliente"),
                conexion = 1
            )
        
            messages.warning(request, "Cliente creado correctamente")
            return redirect('registro_clientes')
        else:
            messages.warning(request, 'No se pudo crear el Cliente')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4
    }

    return render(request, 'usuarios/registro_clientes.html', context)