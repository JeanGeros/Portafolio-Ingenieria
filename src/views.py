from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib import messages
from src.forms import (
    FormClienteNormal1, FormClienteNormal2, FormClienteNormal3, addproductsForm
)

from .models import (
    Persona, Direccion, Usuario, Cliente, Estado, Comuna, Tipobarrio, Tipovivienda, Rolusuario, 
    Proveedor, Tipoproducto, Producto, Familiaproducto
)

def Index(request):

    context = {

    }

    return render(request, 'index.html', context)

def Ingreso(request):

    if request.method == 'POST':

        username = request.POST.get('usuario')
        password = request.POST.get('contraseña')

        usuario_correo = Usuario.objects.filter(nombreusuario=username).exists()

        if usuario_correo == True:

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                messages.warning(request, 'Email y/o contraseña inválidos.')
        else:
            messages.warning(request, 'Email y/o contraseña inválidos.')

    context = {

    }

    return render(request, 'ingreso/ingreso_usuarios.html', context)

def addProducts(request):

    old_post_ingreso = request.session.get('old_post_ingreso') 
    old_post_conexion = request.session.get('old_post_conexion') 

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

        cerrar_sesion = request.POST.get('cerrar_sesion')

        if cerrar_sesion == "CerrarSesion":
            usuario = Usuario.objects.get(email=old_post_ingreso['correo'])
            usuario.conexion = 0
            usuario.save()
            request.session['old_post_ingreso'] = request.POST
            request.session['old_post_conexion'] = {'conexion':usuario.conexion}
            return render(request, 'index.html', context)

    context = {
        'form': form,
        'correo': old_post_ingreso['correo'],
        'conexion': old_post_conexion['conexion']
    }

    return render(request, 'Modulo_productos/addProducts.html', context)

def listar_productos(request):

    productos = Producto.objects.all()
    
    context = {
        'productos': productos
    }

    return render(request, 'Modulo_productos/listarProductos.html', context)

##********************Clientes*******************************************************************

def Registro_clientes(request):
    
    form1 = FormClienteNormal1()
    form2 = FormClienteNormal2()
    form3 = FormClienteNormal3()

    if request.method == 'POST':
        
        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellidopaterno')
        apellido_materno = request.POST.get('apellidomaterno')
        telefono = request.POST.get('telefono')
        nombre_usuario = request.POST.get('nombreusuario')
        email = request.POST.get('email')
        calle = request.POST.get('calle')
        numero = request.POST.get('numero')
        comuna_id = request.POST.get('comunaid')
        tipo_vivienda_id = request.POST.get('tipoviviendaid')
        tipo_barrio_id = request.POST.get('tipobarrioid')
        nombre_sector = request.POST.get('nombresector')
        contraseña = request.POST.get('password')
        confirme_contraseña = request.POST.get('confirme_contraseña')

        user = User.objects.create_user(
            username = nombre_usuario,
            first_name = nombres,
            last_name = apellido_paterno,
            email = email,
            is_superuser = False,
            is_active = True
        )
        user.set_password(contraseña)
        user.set_password(confirme_contraseña)

        if user is not None:
            user.save()
        
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
            nombreusuario = nombre_usuario
        )

        if Cliente is not None:
            messages.warning(request, "Cliente creado correctamente")
            return redirect('registro_clientes')
        else:
            messages.warning(request, 'No se pudo crear el Cliente')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'clientes/registro_clientes.html', context)

def Listar_clientes(request):

    clientes = Cliente.objects.all()

    if request.method == 'POST':

        if request.POST.get('CambiarEstado') is not None:
            id_cliente = request.POST.get('CambiarEstado')
            Cambiar_estado_cliente(id_cliente)
            cliente = Cliente.objects.get(clienteid = id_cliente)
            messages.warning(request, f'El cliente {cliente.personaid.runcuerpo} - {cliente.personaid.dv} ha quedado {cliente.estadoid.descripcion} correctamente')
            return redirect('listar_clientes')
        
        if request.POST.get('VerCliente') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_cliente')

        if request.POST.get('EditarCliente') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('editar_cliente')

    context = {
        'clientes':clientes,
    }

    return render(request, 'clientes/listar_clientes.html', context)

def Cambiar_estado_cliente(id_cliente):

    cliente = Cliente.objects.get(clienteid = id_cliente)

    if cliente.estadoid.descripcion == 'Activo':
        cliente.estadoid = Estado.objects.get(descripcion = "Inactivo")
        cliente.save()
    else: 
        cliente.estadoid = Estado.objects.get(descripcion = "Activo")
        cliente.save()

def Ver_cliente(request):

    old_post_ingreso = request.session.get('old_post_ingreso') 
    old_post_conexion = request.session.get('old_post_conexion') 

    old_post = request.session.get('_old_post')
    cliente = Cliente.objects.get(clienteid=old_post['VerCliente'])

    context = {
        'cliente':cliente
    }

    return render(request, 'clientes/ver_cliente.html', context)

def Editar_cliente(request):

    old_post = request.session.get('_old_post')

    cliente = Cliente.objects.filter(clienteid=old_post['EditarCliente']).values('personaid','direccionid')
    cliente_usuario = Usuario.objects.get(personaid=cliente[0]['personaid'])
    cliente_persona = Persona.objects.get(personaid=cliente[0]['personaid'])
    cliente_direccion = Direccion.objects.get(direccionid=cliente[0]['direccionid'])

    form1 = FormClienteNormal1(request.POST or None, instance=cliente_persona)
    form2 = FormClienteNormal2(request.POST or None, instance=cliente_direccion)
    form3 = FormClienteNormal3(request.POST or None, instance=cliente_usuario)

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

        cliente_persona.runcuerpo = run_cuerpo
        cliente_persona.save()
        cliente_persona.dv = dv
        cliente_persona.save()
        cliente_persona.apellidopaterno = apellido_paterno
        cliente_persona.save()
        cliente_persona.apellidomaterno = apellido_materno
        cliente_persona.save()
        cliente_persona.nombres = nombres
        cliente_persona.save()
        cliente_persona.telefono = telefono
        cliente_persona.save()

        cliente_direccion.calle = calle
        cliente_direccion.save()
        cliente_direccion.numero = numero
        cliente_direccion.save()
        cliente_direccion.comunaid = Comuna.objects.get(comunaid=comuna_id)
        cliente_direccion.save()
        cliente_direccion.tipoviviendaid = Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id)
        cliente_direccion.save()
        cliente_direccion.tipobarrioid = Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id)
        cliente_direccion.save()
        cliente_direccion.nombresector = nombre_sector
        cliente_direccion.save()

        cliente_usuario.email = email

        messages.warning(request, 'Cliente actualizado correctamente')
        return redirect('listar_clientes')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
    }

    return render(request, 'clientes/editar_cliente.html', context)

##******************************************************************************************
