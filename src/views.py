import email
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import sweetify
import datetime 


import qrcode 


from django.contrib import messages
from src.forms import (
    FormClienteNormal1, FormClienteNormal2, FormClienteNormal3, addproductsForm, FormVendedorPersona,
    FormVendedorUsuario, FormVendedorEmpleado, FormEmpleadoPersona, FormEmpleadoUsuario, FormEmpleadoEmpleado,
    FormProveedor
)

from .models import (
    Detalleorden, Estadoorden, Ordencompra, Persona, Direccion, Usuario, Cliente, Estado, Comuna, Tipobarrio, Tipovivienda, Rolusuario,
    Proveedor, Tipoproducto, Producto, Familiaproducto, Empleado, Cargo, Tiporubro
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

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                sweetify.success(request, 'Ingreso realizado con exito')
                return render(request, 'index.html')
            else:
                sweetify.warning(request, 'Usuario y/o contraseña inválidos.')
        else:
            sweetify.warning(request, 'Usuario y/o contraseña inválidos.')

    context = {

    }

    return render(request, 'ingreso/ingreso_usuarios.html', context)

#************************************Productos*********************************************
def Agregar_productos(request):
    form = addproductsForm(request.POST, request.FILES)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        stockcritico = request.POST.get('stockcritico')
        fechavencimiento = request.POST.get('fechavencimiento')
        imagen = request.FILES.get('imagen')
        proveedorid = request.POST.get('proveedorid')
        tipoproductoid = request.POST.get('tipoproductoid')
        familiaproid = request.POST.get('familiaproid')
        estadoid = request.POST.get('estadoid')

        proveedor = Proveedor.objects.get(proveedorid=proveedorid)
        tipo_producto = Tipoproducto.objects.get(tipoproductoid=tipoproductoid)
        familia_producto = Familiaproducto.objects.get(familiaproid=familiaproid)
        Estado_producto = Estado.objects.get(estadoid=estadoid)

        if len(fechavencimiento) == 10:  
            fecha = fechavencimiento.split("/")
            fechavencimiento = f"{fecha[2]}-{fecha[1]}-{fecha[0]}"
            fechacodigo = f"{fecha[2]}{fecha[1]}{fecha[0]}"
        else:
            fechavencimiento = None
            fechacodigo = "00000000"    

        codigo = f"{proveedor.proveedorid}{familia_producto.familiaproid}{fechacodigo}{tipo_producto.tipoproductoid}"
        try:
            product = Producto.objects.create(
                nombre=nombre.strip(),
                precio=precio.strip(),
                stock=stock.strip(),
                stockcritico=stockcritico.strip(),
                fechavencimiento=fechavencimiento,
                codigo=codigo,
                imagen=imagen,
                proveedorid=proveedor,
                tipoproductoid=tipo_producto,
                familiaproid=familia_producto,
                estadoid=Estado_producto
            )

            if product is not None:
                sweetify.success(request, 'Producto creado correctamente')
                return redirect('listar_productos')

        except Exception as error:
            sweetify.warning(request, error)

    context = {
        'form': form,
    }

    return render(request, 'productos/agregar_productos.html', context)


def Listar_productos(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        if request.POST.get('CambiarEstado') is not None:
            id_producto = request.POST.get('CambiarEstado')
            Cambiar_estado_producto(id_producto)
            producto = Producto.objects.get(productoid=id_producto)
            sweetify.success(request,
                             f'El producto {producto.nombre} ha quedado {producto.estadoid.descripcion} correctamente')
            return redirect('listar_productos')
        
        if request.POST.get('VerProducto') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_producto')

        if request.POST.get('EditarProducto') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('editar_producto')
    
    context = {
        'productos': productos
    }

    return render(request, 'productos/listar_productos.html', context)


def Cambiar_estado_producto(id_producto):
    producto = Producto.objects.get(productoid=id_producto)

    if producto.estadoid.descripcion == 'Activo':
        producto.estadoid = Estado.objects.get(descripcion="Inactivo")
        producto.save()
    else: 
        producto.estadoid = Estado.objects.get(descripcion="Activo")
        producto.save()


def Ver_producto(request):
    old_post = request.session.get('_old_post')
    producto = Producto.objects.get(productoid=old_post['VerProducto'])

    context = {
        'producto': producto,
    }

    return render(request, 'productos/ver_producto.html', context)


def Editar_producto(request):
    old_post = request.session.get('_old_post')

    producto = Producto.objects.get(productoid=old_post['EditarProducto'])

    form = addproductsForm(request.POST or None, instance=producto)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        stockcritico = request.POST.get('stockcritico')
        fechavencimiento = request.POST.get('fechavencimiento')
        imagen = request.FILES.get('imagen')
        proveedorid = request.POST.get('proveedorid')
        tipoproductoid = request.POST.get('tipoproductoid')
        familiaproid = request.POST.get('familiaproid')
        estadoid = request.POST.get('estadoid')
        proveedor = Proveedor.objects.get(proveedorid=proveedorid)
        tipo_producto = Tipoproducto.objects.get(tipoproductoid=tipoproductoid)
        familia_producto = Familiaproducto.objects.get(familiaproid=familiaproid)
        Estado_producto = Estado.objects.get(estadoid=estadoid)

        fecha = fechavencimiento.split("/")
        if len(fechavencimiento) == 10:  
            fechavencimiento = f"{fecha[2]}-{fecha[1]}-{fecha[0]}"
            fechacodigo = f"{fecha[2]}{fecha[1]}{fecha[0]}"
        else:
            fechavencimiento = None
            fechacodigo = "00000000"

        codigo = f"{proveedor.proveedorid}{familia_producto.familiaproid}{fechacodigo}{tipo_producto.tipoproductoid}"

        producto, created = Producto.objects.get_or_create(productoid=old_post['EditarProducto'])
        try:
            producto.nombre = nombre 
            producto.precio = precio
            producto.stock = stock
            producto.stockcritico = stockcritico
            producto.fechavencimiento = fechavencimiento
            producto.proveedorid = proveedor
            producto.tipoproductoid = tipo_producto
            producto.familiaproid = familia_producto
            producto.estadoid = Estado_producto
            producto.codigo = codigo
            producto.imagen = imagen
            producto.save()

            sweetify.success(request, 'Producto actualizado correctamente')
            return redirect('listar_productos')
            
        except Exception as error:
            print(error)
            sweetify.error(request, error)

    context = {
        'form': form,
    }

    return render(request, 'productos/editar_productos.html', context)

#*********************************Clientes*************************************************
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

        personaRegistro = Persona.objects.filter(runcuerpo=run_cuerpo, dv=dv).exists()
        usuarioRegistro = Usuario.objects.filter(email=email).exists()
        usuarioRegistro3 = Usuario.objects.filter(nombreusuario=nombre_usuario).exists()

        if personaRegistro == True:
            sweetify.warning(request, "El run ingresado ya existe")
        elif usuarioRegistro == True:
            sweetify.warning(request, "El correo ingresado ya existe")
        elif usuarioRegistro3 == True:
            sweetify.warning(request, "El usuario ingresado ya esta registrado")
        else: 
            user = User.objects.create_user(
                username=nombre_usuario,
                first_name=nombres,
                last_name=apellido_paterno,
                email=email,
                is_superuser=False,
                is_active=True
            )
            user.set_password(contraseña)
            user.set_password(confirme_contraseña)
            
            # Estado activo = 1 e inactivo = 2 
            Persona.objects.create(
                runcuerpo=run_cuerpo,
                dv=dv,
                apellidopaterno=apellido_paterno,
                apellidomaterno=apellido_materno,
                nombres=nombres,
                telefono=telefono,
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            ValidarDireccion = Direccion.objects.filter(calle=calle,
                                                        numero=numero,
                                                        tipoviviendaid=tipo_vivienda_id).exists()

            if ValidarDireccion == False:
                Direccion.objects.create(
                    calle=calle,
                    numero=numero,
                    comunaid=Comuna.objects.get(comunaid=comuna_id),
                    tipoviviendaid=Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id),
                    tipobarrioid=Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id),
                    nombresector=nombre_sector
                )

            Cliente.objects.create(
                direccionid=Direccion.objects.get(calle=calle, numero=numero),
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            Usuario.objects.create(
                email=email,
                password=contraseña,
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                rolid=Rolusuario.objects.get(descripcion="Cliente"),
                nombreusuario=nombre_usuario
            )

            if (Persona is not None and 
                    Direccion is not None and
                    Usuario is not None and
                Cliente is not None and 
                user is not None):
                
                user.save()

                sweetify.success(request, "Se ha registrado correctamente")
                return redirect('index')
            else:
                sweetify.error(request, "No es posible registrarse en este momento")

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'clientes/registro_clientes.html', context)


def Agregar_cliente(request):
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

        personaRegistro = Persona.objects.filter(runcuerpo=run_cuerpo, dv=dv).exists()
        usuarioRegistro = Usuario.objects.filter(email=email).exists()
        usuarioRegistro3 = Usuario.objects.filter(nombreusuario=nombre_usuario).exists()

        if personaRegistro == True:
            sweetify.warning(request, "El run ingresado ya existe")
        elif usuarioRegistro == True:
            sweetify.warning(request, "El correo ingresado ya existe")
        elif usuarioRegistro3 == True:
            sweetify.warning(request, "El cliente ya cuenta con un usuario")
        else: 
            user = User.objects.create_user(
                username=nombre_usuario,
                first_name=nombres,
                last_name=apellido_paterno,
                email=email,
                is_superuser=False,
                is_active=True
            )
            user.set_password(contraseña)
            user.set_password(confirme_contraseña)
            
            # Estado activo = 1 e inactivo = 2 
            Persona.objects.create(
                runcuerpo=run_cuerpo,
                dv=dv,
                apellidopaterno=apellido_paterno,
                apellidomaterno=apellido_materno,
                nombres=nombres,
                telefono=telefono,
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            ValidarDireccion = Direccion.objects.filter(calle=calle,
                                                        numero=numero,
                                                        tipoviviendaid=tipo_vivienda_id).exists()

            if ValidarDireccion == False:
                Direccion.objects.create(
                    calle=calle,
                    numero=numero,
                    comunaid=Comuna.objects.get(comunaid=comuna_id),
                    tipoviviendaid=Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id),
                    tipobarrioid=Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id),
                    nombresector=nombre_sector
                )

            Cliente.objects.create(
                direccionid=Direccion.objects.get(calle=calle, numero=numero),
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            Usuario.objects.create(
                email=email,
                password=contraseña,
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                rolid=Rolusuario.objects.get(descripcion="Cliente"),
                nombreusuario=nombre_usuario
            )

            if (Persona is not None and 
                Direccion is not None and 
                Usuario is not None and 
                    Cliente is not None and
                user is not None):
                
                user.save()
                
                sweetify.success(request, "Cliente creado correctamente")
                return redirect('registro_clientes')
            else:
                sweetify.error(request, "No es posible crear el cliente en este momento")

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'clientes/agregar_cliente.html', context)


def Listar_clientes(request):
    clientes = Cliente.objects.all()

    if request.method == 'POST':

        if request.POST.get('CambiarEstado') is not None:
            id_cliente = request.POST.get('CambiarEstado')
            Cambiar_estado_cliente(id_cliente)
            cliente = Cliente.objects.get(clienteid=id_cliente)
            sweetify.success(request,
                             f'El cliente {cliente.personaid.runcuerpo} - {cliente.personaid.dv} ha quedado {cliente.estadoid.descripcion} correctamente')
            return redirect('listar_clientes')
        
        if request.POST.get('VerCliente') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_cliente')

        if request.POST.get('EditarCliente') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('editar_cliente')

    context = {
        'clientes': clientes,
    }

    return render(request, 'clientes/listar_clientes.html', context)


def Cambiar_estado_cliente(id_cliente):
    cliente = Cliente.objects.get(clienteid=id_cliente)
    persona_id = Cliente.objects.filter(clienteid=id_cliente).values('personaid')
    usuario = Usuario.objects.filter(personaid=persona_id[0]['personaid']).values('nombreusuario')
    user = User.objects.get(username=usuario[0]['nombreusuario'])

    if cliente.estadoid.descripcion == 'Activo':
        cliente.estadoid = Estado.objects.get(descripcion="Inactivo")
        cliente.save()
        user.is_active = False
        user.save()
    else: 
        cliente.estadoid = Estado.objects.get(descripcion="Activo")
        cliente.save()
        user.is_active = True
        user.save()


def Ver_cliente(request):
    old_post = request.session.get('_old_post')
    cliente = Cliente.objects.get(clienteid=old_post['VerCliente'])

    context = {
        'cliente': cliente
    }

    return render(request, 'clientes/ver_cliente.html', context)


def Editar_cliente(request):
    old_post = request.session.get('_old_post')

    cliente = Cliente.objects.filter(clienteid=old_post['EditarCliente']).values('personaid', 'direccionid')
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
        # nombre_usuario = request.POST.get('nombreusuario')
        print(run_cuerpo)

        cliente_persona, created = Persona.objects.get_or_create(personaid=cliente[0]['personaid'])
        cliente_persona.runcuerpo = run_cuerpo
        cliente_persona.dv = dv
        cliente_persona.apellidopaterno = apellido_paterno
        cliente_persona.apellidomaterno = apellido_materno
        cliente_persona.nombres = nombres
        cliente_persona.telefono = telefono
        cliente_persona.save()

        cliente_direccion, created = Direccion.objects.get_or_create(direccionid=cliente[0]['direccionid'])
        cliente_direccion.calle = calle
        cliente_direccion.numero = numero
        cliente_direccion.comunaid = Comuna.objects.get(comunaid=comuna_id)
        cliente_direccion.tipoviviendaid = Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id)
        cliente_direccion.tipobarrioid = Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id)
        cliente_direccion.nombresector = nombre_sector
        cliente_direccion.save()

        cliente_usuario, created = Usuario.objects.get_or_create(personaid=cliente[0]['personaid'])
        cliente_usuario.email = email
        cliente_usuario.save()

        user_django = User.objects.get(email=cliente_usuario)
        user_django.username = user_django.username
        user_django.first_name = nombres
        user_django.last_name = apellido_paterno
        user_django.email = email
        user_django.save()

        sweetify.success(request, "Cliente actualizado correctamente")
        return redirect('listar_clientes')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
    }

    return render(request, 'clientes/editar_cliente.html', context)

#********************************Vendedores************************************************
def Listar_vendedores(request):
    vendedores = Cargo.objects.get(descripcion="Vendedor")
    vendedores = Empleado.objects.filter(cargoid=vendedores)

    if request.method == 'POST':

        if request.POST.get('CambiarEstado') is not None:
            id_vendedor = request.POST.get('CambiarEstado')
            Cambiar_estado_vendedor(id_vendedor)
            vendedor = Empleado.objects.get(empleadoid=id_vendedor)
            sweetify.success(request,
                             f'El vendedor {vendedor.personaid.runcuerpo} - {vendedor.personaid.dv} ha quedado {vendedor.estadoid.descripcion} correctamente')
            return redirect('listar_vendedores')

        if request.POST.get('VerVendedor') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_vendedor')

        if request.POST.get('EditarVendedor') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('editar_vendedor')

    context = {
        'vendedores': vendedores
    }

    return render(request, 'vendedores/listar_vendedores.html', context)


def Agregar_vendedor(request):
    form1 = FormVendedorPersona()
    form2 = FormVendedorUsuario()
    form3 = FormVendedorEmpleado()

    if request.method == 'POST':
        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellidopaterno')
        apellido_materno = request.POST.get('apellidomaterno')
        telefono = request.POST.get('telefono')
        nombre_usuario = request.POST.get('nombreusuario')
        fecha_ingreso = request.POST.get('fechaingreso')
        email = request.POST.get('email')
        contraseña = request.POST.get('password')
        confirme_contraseña = request.POST.get('confirme_contraseña')

        fecha_ingreso = fecha_ingreso[6:10] + '-' + fecha_ingreso[3:5] + '-' + fecha_ingreso[0:2]

        personaRegistro = Persona.objects.filter(runcuerpo=run_cuerpo, dv=dv).exists()
        usuarioRegistro = Usuario.objects.filter(email=email).exists()
        usuarioRegistro3 = Usuario.objects.filter(nombreusuario=nombre_usuario).exists()

        if personaRegistro:
            sweetify.error(request, "El run ingresado ya existe")

        elif usuarioRegistro:
            sweetify.error(request, "El correo ingresado ya existe")

        elif usuarioRegistro3:
            sweetify.error(request, "El vendedor ya cuenta con un usuario")

        else:
            user = User.objects.create_user(
                username=nombre_usuario,
                first_name=nombres,
                last_name=apellido_paterno,
                email=email,
                is_superuser=False,
                is_active=True
            )
            user.set_password(contraseña)
            user.set_password(confirme_contraseña)
            
            # Estado activo = 1 e inactivo = 2 
            Persona.objects.create(
                runcuerpo=run_cuerpo,
                dv=dv,
                apellidopaterno=apellido_paterno,
                apellidomaterno=apellido_materno,
                nombres=nombres,
                telefono=telefono,
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            Usuario.objects.create(
                email=email,
                password=contraseña,
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                rolid=Rolusuario.objects.get(descripcion="Vendedor"),
                nombreusuario=nombre_usuario
            )

            Empleado.objects.create(
                fechaingreso=fecha_ingreso,
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                cargoid=Cargo.objects.get(descripcion="Vendedor"),
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            if (Persona is not None and
                    Usuario is not None and
                    Empleado is not None and
                    user is not None):

                user.save()
                sweetify.success(request, "Vendedor creado correctamente")
                return redirect('listar_vendedores')

            else:
                sweetify.error(request, "No es posible crear el vendedor en este momento")

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'vendedores/agregar_vendedor.html', context)


def Ver_vendedor(request):
    old_post = request.session.get('_old_post')
    vendedor = Empleado.objects.get(empleadoid=old_post['VerVendedor'])

    context = {
        'vendedor': vendedor
    }

    return render(request, 'vendedores/ver_vendedor.html', context)


def Editar_vendedor(request):
    old_post = request.session.get('_old_post')

    vendedor = Empleado.objects.filter(empleadoid=old_post['EditarVendedor']).values('personaid')
    vendedor_usuario = Usuario.objects.get(personaid=vendedor[0]['personaid'])
    vendedor_persona = Persona.objects.get(personaid=vendedor[0]['personaid'])
    vendedor_empleado = Empleado.objects.get(personaid=vendedor[0]['personaid'])

    form1 = FormVendedorPersona(request.POST or None, instance=vendedor_persona)
    form2 = FormVendedorUsuario(request.POST or None, instance=vendedor_usuario)
    form3 = FormVendedorEmpleado(request.POST or None, instance=vendedor_empleado)

    if request.method == 'POST':
        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellidopaterno')
        apellido_materno = request.POST.get('apellidomaterno')
        telefono = request.POST.get('telefono')
        nombre_usuario = request.POST.get('nombreusuario')
        fecha_ingreso = request.POST.get('fechaingreso')
        email = request.POST.get('email')

        fecha_ingreso = fecha_ingreso[6:10] + '-' + fecha_ingreso[3:5] + '-' + fecha_ingreso[0:2]

        empleado, created = Empleado.objects.get_or_create(empleadoid=old_post['EditarVendedor'])
        empleado.fechaingreso = fecha_ingreso 
        empleado.personaid.runcuerpo = run_cuerpo
        empleado.personaid.dv = dv
        empleado.personaid.nombres = nombres
        empleado.personaid.apellidopaterno = apellido_paterno
        empleado.personaid.apellidomaterno = apellido_materno
        empleado.personaid.telefono = telefono
        empleado.save()

        empleado_para_persona = Empleado.objects.filter(empleadoid=old_post['EditarVendedor']).values('personaid')
        usuario, created = Usuario.objects.get_or_create(personaid=empleado_para_persona[0]['personaid'])
        usuario.nombreusuario = nombre_usuario 
        usuario.email = email
        usuario.save() 

        persona, created = Persona.objects.get_or_create(personaid=empleado_para_persona[0]['personaid'])
        persona.runcuerpo = run_cuerpo 
        persona.dv = dv 
        persona.apellidopaterno = apellido_paterno 
        persona.apellidomaterno = apellido_materno 
        persona.nombres = nombres 
        persona.telefono = telefono 
        persona.save()

        user_django = User.objects.get(email=vendedor_usuario)
        user_django.username = user_django.username
        user_django.first_name = nombres
        user_django.last_name = apellido_paterno
        user_django.email = email
        user_django.save()

        sweetify.success(request, "Vendedor actualizado correctamente")
        return redirect('listar_vendedores')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'vendedores/editar_vendedor.html', context)


def Cambiar_estado_vendedor(id_vendedor):
    vendedor = Empleado.objects.get(empleadoid=id_vendedor)
    persona_id = Empleado.objects.filter(empleadoid=id_vendedor).values('personaid')
    usuario = Usuario.objects.filter(personaid=persona_id[0]['personaid']).values('nombreusuario')
    user = User.objects.get(username=usuario[0]['nombreusuario'])

    if vendedor.estadoid.descripcion == 'Activo':
        vendedor.estadoid = Estado.objects.get(descripcion="Inactivo")
        vendedor.save()
        user.is_active = False
        user.save()
    else:
        vendedor.estadoid = Estado.objects.get(descripcion="Activo")
        vendedor.save()
        user.is_active = True
        user.save()

#********************************Vendedores************************************************
def Agregar_proveedor(request):
    old_post_ingreso = request.session.get('old_post_ingreso') 
    old_post_conexion = request.session.get('old_post_conexion') 

    form = FormProveedor()

    if request.method == 'POST':
        razonsocial = request.POST.get('razonsocial')
        rutcuerpo = request.POST.get('rutcuerpo')
        dv = request.POST.get('dv')
        fono = request.POST.get('fono')
        rubroid = request.POST.get('rubroid')
        direccionid = request.POST.get('direccionid')
        estadoid = request.POST.get('estadoid')

        rubro = Tiporubro.objects.get(rubroid=rubroid)
        direccion = Direccion.objects.get(direccionid=direccionid)
        estado = Estado.objects.get(estadoid=estadoid)

        proveedor = Proveedor.objects.create(
            razonsocial=razonsocial.strip(),
            rutcuerpo=rutcuerpo.strip(),
            dv=dv.strip(),
            fono=fono.strip(),
            direccionid=direccion,
            estadoid=estado,
            rubroid=rubro,
        )
        
        if proveedor is not None:
            messages.warning(request, 'Proveedor creado correctamente')
            return redirect('listar_proveedores')
        else:
            messages.warning(request, 'No se pudo crear el Producto')

    context = {
        'form': form,
    }

    return render(request, 'proveedores/agregar_proveedor.html', context)


def Cambiar_estado_proveedor(id_proveedor):
    proveedor = Proveedor.objects.get(proveedorid=id_proveedor)
    if proveedor.estadoid.descripcion == 'Activo':
        proveedor.estadoid = Estado.objects.get(descripcion="Inactivo")
        proveedor.save()
    else: 
        proveedor.estadoid = Estado.objects.get(descripcion="Activo")
        proveedor.save()


def Listar_proveedores(request):
    proveedor = Proveedor.objects.all()

    if request.method == 'POST':
        if request.POST.get('CambiarEstado') is not None:
            id_proveedor = request.POST.get('CambiarEstado')
            Cambiar_estado_proveedor(id_proveedor)
            proveedor = Proveedor.objects.get(proveedorid=id_proveedor)
            messages.warning(request,
                             f'El producto {proveedor.razonsocial} ha quedado {proveedor.estadoid.descripcion} correctamente')
            return redirect('listar_proveedores')
        
        if request.POST.get('VerProveedor') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_proveedor')

        if request.POST.get('EditarProveedor') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('editar_proveedor')
    
    context = {
        'proveedor': proveedor
    }

    return render(request, 'proveedores/listar_proveedores.html', context)


def Ver_proveedor(request):
    old_post = request.session.get('_old_post')
    proveedor = Proveedor.objects.get(proveedorid=old_post['VerProveedor'])

    context = {
        'proveedor': proveedor,
    }

    return render(request, 'proveedores/ver_proveedor.html', context)


def Editar_proveedor(request):
    old_post_ingreso = request.session.get('_old_post_ingreso') 
    old_post_conexion = request.session.get('_old_post_conexion') 

    old_post = request.session.get('_old_post')

    proveedor = Proveedor.objects.get(proveedorid=old_post['EditarProveedor'])
    form = FormProveedor(request.POST or None, instance=proveedor)

    if request.method == 'POST':
        razonsocial = request.POST.get('razonsocial')
        rutcuerpo = request.POST.get('rutcuerpo')
        dv = request.POST.get('dv')
        fono = request.POST.get('fono')
        rubroid = request.POST.get('rubroid')
        direccionid = request.POST.get('direccionid')
        estadoid = request.POST.get('estadoid')

        rubro = Tiporubro.objects.get(rubroid=rubroid)
        direccion = Direccion.objects.get(direccionid=direccionid)
        estado = Estado.objects.get(estadoid=estadoid)

        proveedor, created = Proveedor.objects.get_or_create(proveedorid=old_post['EditarProveedor'])
        try:
            proveedor.razonsocial = razonsocial 
            proveedor.rutcuerpo = rutcuerpo
            proveedor.dv = dv
            proveedor.fono = fono
            proveedor.rubroid = rubro
            proveedor.direccionid = direccion
            proveedor.estadoid = estado
            proveedor.save()

            messages.warning(request, 'Proveedor actualizado correctamente')
            return redirect('listar_proveedores')
            
        except Exception as error:
            print(error)
            messages.error(request, error)

    context = {
        'form': form,
    }

    return render(request, 'proveedores/editar_proveedor.html', context)

#********************************Empleados************************************************

def Listar_empleados(request):
    empleados = Cargo.objects.get(descripcion="Empleado")
    empleados = Empleado.objects.filter(cargoid=empleados)

    if request.method == 'POST':

        if request.POST.get('CambiarEstado') is not None:
            id_empleado = request.POST.get('CambiarEstado')
            Cambiar_estado_empleado(id_empleado)
            empleado = Empleado.objects.get(empleadoid=id_empleado)
            sweetify.success(request,
                             f'El empleado {empleado.personaid.runcuerpo} - {empleado.personaid.dv} ha quedado {empleado.estadoid.descripcion} correctamente')
            return redirect('listar_empleados')

        if request.POST.get('VerEmpleado') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_empleado')

        if request.POST.get('EditarEmpleado') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('editar_empleado')

    context = {
        'empleados': empleados
    }

    return render(request, 'empleados/listar_empleados.html', context)


def Agregar_empleado(request):
    form1 = FormEmpleadoPersona()
    form2 = FormEmpleadoUsuario()
    form3 = FormEmpleadoEmpleado()

    if request.method == 'POST':
        
        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellidopaterno')
        apellido_materno = request.POST.get('apellidomaterno')
        telefono = request.POST.get('telefono')
        nombre_usuario = request.POST.get('nombreusuario')
        fecha_ingreso = request.POST.get('fechaingreso')
        email = request.POST.get('email')
        contraseña = request.POST.get('password')
        confirme_contraseña = request.POST.get('confirme_contraseña')

        fecha_ingreso = fecha_ingreso[6:10] + '-' + fecha_ingreso[3:5] + '-' + fecha_ingreso[0:2]

        personaRegistro = Persona.objects.filter(runcuerpo=run_cuerpo, dv=dv).exists()
        usuarioRegistro = Usuario.objects.filter(email=email).exists()
        usuarioRegistro3 = Usuario.objects.filter(nombreusuario=nombre_usuario).exists()

        if personaRegistro:
            sweetify.error(request, "El run ingresado ya existe")

        elif usuarioRegistro:
            sweetify.error(request, "El correo ingresado ya existe")

        elif usuarioRegistro3:
            sweetify.error(request, "El empleado ya cuenta con un usuario")

        else:
            user = User.objects.create_user(
                username=nombre_usuario,
                first_name=nombres,
                last_name=apellido_paterno,
                email=email,
                is_superuser=False,
                is_active=True
            )
            user.set_password(contraseña)
            user.set_password(confirme_contraseña)
            
            # Estado activo = 1 e inactivo = 2 
            Persona.objects.create(
                runcuerpo=run_cuerpo,
                dv=dv,
                apellidopaterno=apellido_paterno,
                apellidomaterno=apellido_materno,
                nombres=nombres,
                telefono=telefono,
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            Usuario.objects.create(
                email=email,
                password=contraseña,
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                rolid=Rolusuario.objects.get(descripcion="Empleado"),
                nombreusuario=nombre_usuario
            )

            Empleado.objects.create(
                fechaingreso=fecha_ingreso,
                personaid=Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                cargoid=Cargo.objects.get(descripcion="Empleado"),
                estadoid=Estado.objects.get(descripcion="Activo")
            )

            if (Persona is not None and 
                Usuario is not None and 
                Empleado is not None and 
                user is not None):

                user.save()
                sweetify.success(request, "Empleado creado correctamente")

                return redirect('listar_empleados')
            else:
                sweetify.warning(request, "No es posible crear el empleado en este momento")

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'empleados/agregar_empleado.html', context)


def Ver_empleado(request):
    old_post = request.session.get('_old_post')
    empleado = Empleado.objects.get(empleadoid=old_post['VerEmpleado'])

    context = {
        'empleado': empleado
    }

    return render(request, 'empleados/ver_empleado.html', context)


def Editar_empleado(request):
    old_post = request.session.get('_old_post')

    empleado = Empleado.objects.filter(empleadoid=old_post['EditarEmpleado']).values('personaid')
    empleado_usuario = Usuario.objects.get(personaid=empleado[0]['personaid'])
    empleado_persona = Persona.objects.get(personaid=empleado[0]['personaid'])
    empleado_empleado = Empleado.objects.get(personaid=empleado[0]['personaid'])

    form1 = FormEmpleadoPersona(request.POST or None, instance=empleado_persona)
    form2 = FormEmpleadoUsuario(request.POST or None, instance=empleado_usuario)
    form3 = FormEmpleadoEmpleado(request.POST or None, instance=empleado_empleado)

    if request.method == 'POST':
        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellidopaterno')
        apellido_materno = request.POST.get('apellidomaterno')
        telefono = request.POST.get('telefono')
        nombre_usuario = request.POST.get('nombreusuario')
        fecha_ingreso = request.POST.get('fechaingreso')
        email = request.POST.get('email')

        fecha_ingreso = fecha_ingreso[6:10] + '-' + fecha_ingreso[3:5] + '-' + fecha_ingreso[0:2]

        empleadoEm, created = Empleado.objects.get_or_create(empleadoid=old_post['EditarEmpleado'])
        empleadoEm.fechaingreso = fecha_ingreso 
        empleadoEm.personaid.runcuerpo = run_cuerpo
        empleadoEm.personaid.dv = dv
        empleadoEm.personaid.nombres = nombres
        empleadoEm.personaid.apellidopaterno = apellido_paterno
        empleadoEm.personaid.apellidomaterno = apellido_materno
        empleadoEm.personaid.telefono = telefono
        empleadoEm.save()

        empleado_para_persona = Empleado.objects.filter(empleadoid=old_post['EditarEmpleado']).values('personaid')
        usuario, created = Usuario.objects.get_or_create(personaid=empleado_para_persona[0]['personaid'])
        usuario.nombreusuario = nombre_usuario 
        usuario.email = email
        usuario.save() 

        persona, created = Persona.objects.get_or_create(personaid=empleado_para_persona[0]['personaid'])
        persona.runcuerpo = run_cuerpo 
        persona.dv = dv 
        persona.apellidopaterno = apellido_paterno 
        persona.apellidomaterno = apellido_materno 
        persona.nombres = nombres 
        persona.telefono = telefono 
        persona.save()

        user_django = User.objects.get(email=empleado_usuario)
        user_django.username = user_django.username
        user_django.first_name = nombres
        user_django.last_name = apellido_paterno
        user_django.email = email
        user_django.save()

        sweetify.success(request, "Empleado actualizado correctamente")
        return redirect('listar_empleados')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'empleados/editar_empleado.html', context)


def Cambiar_estado_empleado(id_empleado):
    empleado = Empleado.objects.get(empleadoid=id_empleado)
    persona_id = Empleado.objects.filter(empleadoid=id_empleado).values('personaid')
    usuario = Usuario.objects.filter(personaid=persona_id[0]['personaid']).values('nombreusuario')
    user = User.objects.get(username=usuario[0]['nombreusuario'])

    if empleado.estadoid.descripcion == 'Activo':
        empleado.estadoid = Estado.objects.get(descripcion="Inactivo")
        empleado.save()
        user.is_active = False
        user.save()
    else: 
        empleado.estadoid = Estado.objects.get(descripcion="Activo")
        empleado.save()
        user.is_active = True
        user.save()

# *********************************Pedidos************************************************
@csrf_exempt
def Crear_pedido(request, id = None):
    proveedor = Proveedor.objects.filter(proveedorid=id)
    for prov in proveedor:
        productos = Producto.objects.filter(proveedorid=prov)
    listaProds = []
    for prod in productos:
        listaProds.append(prod.nombre)

    if request.method == 'POST':
        listaProductos = []
        for key,value in request.POST.items():
            print(f"key: {key}  value  {value}")
            try:
                nomProduct = Producto.objects.get(nombre=key)
                idProduct = nomProduct.productoid
                if len(listaProductos) == 0 :
                    listaProductos.append({'id':idProduct, 'value':value})
                else:
                    for product in listaProductos:
                        if product['id'] == str(idProduct):
                            print("found")
                            sum_value = int(product['value']) + int(value)
                            product.update({'value': sum_value})
                            break
                        else:
                            print("not found")
                            listaProductos.append({'id':idProduct, 'value':value})
                            break

            except Producto.DoesNotExist:
                if key == "fecha_vencimiento" and len(value) == 0:
                    fecha = "1000-10-10"
                else:
                    fecha=value

        proveedorOrden = Proveedor.objects.get(proveedorid=int(id))
        estado_orden = Estadoorden.objects.get(estadoordenid=1)
        
        ordenPedido = Ordencompra.objects.create(
            fechapedido = fecha,
            proveedorid = proveedorOrden,
            estadoordenid = estado_orden
        )

        last_orden_compra = Ordencompra.objects.order_by('ordenid').last()
        print(listaProductos)

        for products in listaProductos:
            producto = Producto.objects.get(productoid= int(products['id']))

            detallePedido = Detalleorden.objects.create(
                productoid = producto,
                cantidad = products['value'],
                ordenid = last_orden_compra
            )

        messages.warning(request, 'Orden de pedido realizada con exito')
        return redirect('listar_pedidos')

    context = {
        'proveedor':proveedor,
        'listaProds':listaProds
    }
    return render(request, 'pedidos/crear_pedido.html', context)


def filtro_proveedor(request):
    proveedores = Proveedor.objects.all()   
    context = {
        'proveedores':proveedores,
    }
    
    return render(request, 'pedidos/crear_pedido_proveedores.html', context)


def cambiar_estado_pedido(id_pedido):
    orden_compra = Ordencompra.objects.get(ordenid=int(id_pedido))

    estado_eliminado = Estadoorden.objects.get(estadoordenid=25)

    if orden_compra.estadoordenid.estadoordenid == 1:
        orden_compra.estadoordenid = estado_eliminado
        orden_compra.save()


def Listar_pedidos(request):
    ordenes = Ordencompra.objects.all()

    if request.method == 'POST':
        if request.POST.get('CambiarEstado') is not None:
            id_pedido = request.POST.get('CambiarEstado')
            print(id_pedido)
            cambiar_estado_pedido(id_pedido)
            orden_compra = Ordencompra.objects.get(ordenid=id_pedido)
            sweetify.success(request,
                             f'La Nro:{orden_compra.ordenid} se elimino correctamente')
            return redirect('listar_pedidos')

        if request.POST.get('VerPedido') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_pedido')

    context = {
        'ordenes': ordenes
    }

    return render(request, 'pedidos/listar_pedidos.html', context)


def Ver_pedidos(request):
    old_post = request.session.get('_old_post')
    print(old_post['VerPedido'])
    detalle_orden = Detalleorden.objects.filter(ordenid=old_post['VerPedido'])
    print(detalle_orden)
    context = {
        'detalle_orden': detalle_orden,
    }

    return render(request, 'pedidos/ver_pedido.html', context)


# ***************************Recepcionar pedidos*******************************************

def RecepcionPedido(request, id = None):

    # usuario = request.user
    # usuario = User.objects.get(username=usuario)

    # seguimientoPag = SEGUIMIENTO_PAGINA.objects.create(
    #     pagina_visitada = "Recepcion de pedidos",
    #     usuario = usuario
    # )
    # seguimientoPag.save()

    # form = FormProveedor(request.POST or None, instance=proveedor)

    if id:
        ordenPedido = Ordencompra.objects.filter(ordenid=id)
        detalleOrden = Detalleorden.objects.filter(ordenid=id)
        productos = Producto.objects.all()
   
    if request.method == 'POST':
        print(request.__dict__)
        cantidad = request.POST.get('cantidad')
        print(cantidad)
        # orden_confirmada = Ordencompra.objects.get(id=id)


        # fecharecepcion = datetime.now().date()
        # cantidad =cantidad
        # ordenid = orden_confirmada
        # proveedorid = orden_confirmada.proveedorid
        # productoid = orden_confirmada

        # ordenPedido3.estado_recepcion = 1
        # ordenPedido3.save()
        # ordenPedido3.fecha_recepcion = fecha
        # ordenPedido3.save()
        # ordenPedido3.hora_recepcion = hora
        # ordenPedido3.save()

        # return redirect('listar_pedidos')

    context= {
        'ordenPedido':ordenPedido,
        'productos':productos,
        'detalleOrden':detalleOrden,
    }

    return render(request, 'recepcion_pedido.html',context)




    usuario = request.user
    usuario = User.objects.get(username=usuario)

    seguimientoPag = SEGUIMIENTO_PAGINA.objects.create(
        pagina_visitada = "Recepcion de pedidos",
        usuario = usuario
    )
    seguimientoPag.save()

    ordenPedido = ORDEN_PEDIDO.objects.all()
    detalleOrden = DETALLE_ORDEN.objects.all()
    productos = ""

    ordenPedido2 = ""
    detalleOrden2 = ""
    if id:
        ordenPedido2 = ORDEN_PEDIDO.objects.filter(id=id)
        detalleOrden2 = DETALLE_ORDEN.objects.filter(orden_pedido=id)
        productos = PRODUCTO.objects.all()

    if request.method == 'POST':

        ordenPedido3 = ORDEN_PEDIDO.objects.get(id=id)
        validado = request.POST.get('validado')
        fecha = datetime.now().date()
        hora = datetime.now().time()
        print(fecha)
        print(hora)

        ordenPedido3.estado_recepcion = 1
        ordenPedido3.save()
        ordenPedido3.fecha_recepcion = fecha
        ordenPedido3.save()
        ordenPedido3.hora_recepcion = hora
        ordenPedido3.save()

        return redirect('RecepcionPedido')

    context= {
        'ordenPedido':ordenPedido,
        'productos':productos,
        'detalleOrden':detalleOrden,
        'ordenPedido2':ordenPedido2,
        'detalleOrden2':detalleOrden2
    }

    return render(request, 'recepcion_pedido.html',context)