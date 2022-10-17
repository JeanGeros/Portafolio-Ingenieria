from copyreg import constructor
import email
from multiprocessing.sharedctypes import Value
from this import d
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import sweetify

import datetime
import qrcode
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from src.forms import (
    FormClienteNormal1, FormClienteNormal2, FormClienteNormal3, addproductsForm, FormVendedorPersona,
    FormVendedorUsuario, FormVendedorEmpleado, FormEmpleadoPersona, FormEmpleadoUsuario, FormEmpleadoEmpleado,
    FormProveedor, FormProductoproveedor, FormBodega, FormCliente, FormTipodocumento, FormVenta
)

from .models import (
    Detalleorden, Estadoorden, Ordencompra, Persona, Direccion, Usuario, Cliente, Estado, Comuna, Tipobarrio,
    Tipovivienda, Rolusuario, Direccioncliente, Empresa, Proveedor, Tipoproducto, Producto, Familiaproducto, 
    Empleado, Cargo, Tiporubro, Recepcion, Productoproveedor, Bodega, Boleta, Factura, Venta, Tipodocumento, Detalleventa
)

def Index(request):
    
    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    context = {
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'index.html', context)

def Ingreso(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    if request.method == 'POST':

        username = request.POST.get('usuario')
        password = request.POST.get('contraseña')

        usuario_correo = Usuario.objects.filter(nombreusuario=username).exists()

        if usuario_correo == True:

            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)
                sweetify.success(request, 'Ingreso realizado con exito')
                return redirect('index')

            else:

                sweetify.warning(request, 'Usuario y/o contraseña inválidos.')
        else:

            sweetify.warning(request, 'Usuario y/o contraseña inválidos.')

    context = {
        'tipo_usuario': tipo_usuario
    }
    
    return render(request, 'ingreso/ingreso_usuarios.html', context)

#************************************Productos*********************************************
@login_required(login_url="ingreso")
def Agregar_productos(request):
    #
    # lugares_ocupados = []
    # producto_bodega = Producto.objects.all().exclude(BodegaId=None).values('BodegaId')
    # for p in list(producto_bodega):
    #     lugares_ocupados.append(p['BodegaId'])

    form = addproductsForm(request.POST, request.FILES)
    form_prov = FormProductoproveedor(request.POST, request.FILES)
    form_bodega = FormBodega(request.POST, request.FILES)

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
        bodega_id = request.POST.get('BodegaId')

        tipo_producto = Tipoproducto.objects.get(tipoproductoid=tipoproductoid)
        familia_producto = Familiaproducto.objects.get(familiaproid=familiaproid)
        estado_producto = Estado.objects.get(estadoid=estadoid)
        proveedor = Proveedor.objects.get(proveedorid=proveedorid)
        bodega = Bodega.objects.get(BodegaId=bodega_id)

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
                tipoproductoid=tipo_producto,
                familiaproid=familia_producto,
                estadoid=estado_producto,
                BodegaId=bodega
            )

            ultimo_producto = Producto.objects.order_by('productoid').last()
            prov_producto = Productoproveedor.objects.create(
                ProId=2,
                productoid=ultimo_producto,
                proveedorid=proveedor
            )

            if product is not None and prov_producto is not None:
                sweetify.success(request, 'Producto creado correctamente')
                return redirect('listar_productos')

        except Exception as error:
            sweetify.warning(request, error)

    context = {
        'form': form,
        'form2': form_prov,
        'form_bodega': form_bodega
    }

    return render(request, 'productos/agregar_productos.html', context)


@login_required(login_url="ingreso")
def Listar_productos(request):
    productos = Productoproveedor.objects.all()

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
        'productos': productos,
    }

    return render(request, 'productos/listar_productos.html', context)

@login_required(login_url="ingreso")
def Cambiar_estado_producto(id_producto):
    producto = Producto.objects.get(productoid=id_producto)

    if producto.estadoid.descripcion == 'Activo':
        producto.estadoid = Estado.objects.get(descripcion="Inactivo")
        producto.save()
    else:
        producto.estadoid = Estado.objects.get(descripcion="Activo")
        producto.save()

@login_required(login_url="ingreso")
def Ver_producto(request):
    old_post = request.session.get('_old_post')
    producto = Productoproveedor.objects.get(productoid=old_post['VerProducto'])
    prov_producto = Productoproveedor.objects.get(productoid=old_post['VerProducto'],
                                                  proveedorid=old_post['proveedor'])
    context = {
        'producto': producto,
        'prov_producto': prov_producto
    }

    return render(request, 'productos/ver_producto.html', context)


@login_required(login_url="ingreso")
def Editar_producto(request):
    old_post = request.session.get('_old_post')

    producto = Producto.objects.get(productoid=old_post['EditarProducto'])
    prov_producto = Productoproveedor.objects.get(productoid=old_post['EditarProducto'],
                                                  proveedorid=old_post['proveedor'])

    form2 = FormProductoproveedor(request.POST or None, instance=prov_producto)
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
        bodega_id = request.POST.get('BodegaId')

        proveedor = Proveedor.objects.get(proveedorid=proveedorid)
        tipo_producto = Tipoproducto.objects.get(tipoproductoid=tipoproductoid)
        familia_producto = Familiaproducto.objects.get(familiaproid=familiaproid)
        Estado_producto = Estado.objects.get(estadoid=estadoid)
        bodega = Bodega.objects.get(BodegaId=bodega_id)

        fecha = fechavencimiento.split("/")
        if len(fechavencimiento) == 10:
            fechavencimiento = f"{fecha[2]}-{fecha[1]}-{fecha[0]}"
            fechacodigo = f"{fecha[2]}{fecha[1]}{fecha[0]}"
        else:
            fechavencimiento = None
            fechacodigo = "00000000"

        codigo = f"{proveedor.proveedorid}{familia_producto.familiaproid}{fechacodigo}{tipo_producto.tipoproductoid}"

        try:
            producto, created = Producto.objects.get_or_create(productoid=old_post['EditarProducto'])
            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock
            producto.stockcritico = stockcritico
            producto.fechavencimiento = fechavencimiento
            producto.tipoproductoid = tipo_producto
            producto.familiaproid = familia_producto
            producto.estadoid = Estado_producto
            producto.codigo = codigo
            producto.BodegaId = bodega

            if imagen:
                producto.imagen = imagen

            producto_prove, created = Productoproveedor.objects.get_or_create(productoid=old_post['EditarProducto'],
                                                                              proveedorid=old_post['proveedor'])
            producto_prove.proveedorid = proveedor

            producto_prove.save()
            producto.save()
            sweetify.success(request, 'Producto actualizado correctamente')
            return redirect('listar_productos')
        except Exception as error:
            print(error)
            sweetify.error(request, error)

    context = {
        'form': form,
        'form2': form2
    }

    return render(request, 'productos/editar_productos.html', context)

# *********************************Clientes*************************************************

def Seleccion_registro(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')
    
    context = {

    }

    return render(request, 'clientes/seleccion_registro.html', context)

@login_required(login_url="ingreso")
def Ver_perfil(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    ver_perfil = request.session.get('_ver_perfil')
    datos_usuario = Usuario.objects.filter(nombreusuario=ver_perfil['VerPerfil']).values('nombreusuario','empresaid','personaid')
    usuario = Usuario.objects.get(nombreusuario=ver_perfil['VerPerfil'])
    persona = Persona.objects.get(personaid=datos_usuario[0]['personaid'])

    if Cliente.objects.filter(personaid=datos_usuario[0]['personaid']).exists():
        cliente = Cliente.objects.get(personaid=datos_usuario[0]['personaid'])
    else:
        cliente = None

    if Empleado.objects.filter(personaid=datos_usuario[0]['personaid']).exists():
        empleado = Empleado.objects.get(personaid=datos_usuario[0]['personaid'])
    else:
        empleado = None

    if datos_usuario[0]['empresaid'] is not None:
        empresa = Empresa.objects.get(empresaid=datos_usuario[0]['empresaid'])
    else:
        empresa = None

    if request.method == 'POST':

        if request.POST.get('EditarPerfil') is not None:
            request.session['_editar_perfil'] = request.POST
            return redirect('editar_perfil')

        if request.POST.get('RevisarCompras') is not None:
            request.session['_revisar_compras'] = request.POST
            return redirect('revisar_compras')

        nombre_usuario = request.POST.get('BajarPerfil')
        
        usuario_desactivar = Usuario.objects.filter(nombreusuario=nombre_usuario).values('personaid')
        usuario_desactivar = usuario_desactivar[0]['personaid']
        estadoid = Estado.objects.get(descripcion="Inactivo")

        persona_in, created = Persona.objects.get_or_create(personaid=usuario_desactivar)
        persona_in.estadoid = estadoid
        persona_in.save()

        if Empleado.objects.filter(personaid=usuario_desactivar).exists():
            empleado_in, created = Empleado.objects.get_or_create(personaid=usuario_desactivar)
            empleado_in.estadoid = estadoid
            empleado_in.save()
        
        if Cliente.objects.filter(personaid=usuario_desactivar).exists():
            cliente_in, created = Cliente.objects.get_or_create(personaid=usuario_desactivar)
            cliente_in.estadoid = estadoid
            cliente_in.save()

        user_django = User.objects.get(username=nombre_usuario)
        user_django.is_active = False
        user_django.save()

        logout(request)
        return redirect('index')

    context = {
        'usuario': usuario,
        'persona': persona,
        'empresa': empresa,
        'cliente': cliente,
        'empleado':empleado,
        'tipo_usuario': tipo_usuario
    }

    return render(request, 'clientes/ver_perfil.html', context)


def Revisar_compras(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    context = {
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'index.html', context)

@login_required(login_url="ingreso")
def Editar_perfil(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    editar_perfil= request.session.get('_editar_perfil')

    persona = Persona.objects.filter(runcuerpo=editar_perfil['run'],dv=editar_perfil['dv']).values('personaid')
    usuario = Usuario.objects.filter(personaid=persona[0]['personaid']).values('empresaid','email')
    if Cliente.objects.filter(personaid=persona[0]['personaid']).exists():
        cliente = Cliente.objects.filter(personaid=persona[0]['personaid']).values('direccionid')
    else: 
        cliente = None

    perfil_usuario = Usuario.objects.get(personaid=persona[0]['personaid'])
    perfil_persona = Persona.objects.get(personaid=persona[0]['personaid'])

    if cliente is not None:
        perfil_direccion = Direccion.objects.get(direccionid=cliente[0]['direccionid'])
    else: 
        perfil_direccion = None

    if Empresa.objects.filter(empresaid=usuario[0]['empresaid']).exists():
        perfil_empresa = Empresa.objects.get(empresaid=usuario[0]['empresaid'])
    else:
        perfil_empresa = None

    form1 = FormClienteNormal1(request.POST or None, instance=perfil_persona)

    if perfil_direccion is not None:
        form2 = FormClienteNormal2(request.POST or None, instance=perfil_direccion)
    else: 
        form2 = None

    form3 = FormClienteNormal3(request.POST or None, instance=perfil_usuario)

    if perfil_empresa is not None:
        form4  = FormClienteEmpresa(request.POST or None, instance=perfil_empresa)
    else:
        form4 = None

    if request.method == 'POST':

        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellidopaterno')
        apellido_materno = request.POST.get('apellidomaterno')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        if perfil_direccion is not None:
            calle = request.POST.get('calle')
            numero = request.POST.get('numero')
            comuna_id = request.POST.get('comunaid')
            tipo_vivienda_id = request.POST.get('tipoviviendaid')
            tipo_barrio_id = request.POST.get('tipobarrioid')
            nombre_sector = request.POST.get('nombresector')
            # nombre_usuario = request.POST.get('nombreusuario')

        if perfil_empresa is not None:
            razon_social = request.POST.get('razonsocial')
            rut_cuerpo = request.POST.get('rutcuerpo')
            dv = request.POST.get('dv')
            fono = request.POST.get('fono')

        perfil_persona, created = Persona.objects.get_or_create(personaid=persona[0]['personaid'])
        perfil_persona.runcuerpo = run_cuerpo
        perfil_persona.dv = dv
        perfil_persona.apellidopaterno = apellido_paterno
        perfil_persona.apellidomaterno = apellido_materno
        perfil_persona.nombres = nombres
        perfil_persona.telefono = telefono
        perfil_persona.save()

        if perfil_direccion is not None:

            perfil_direccion, created = Direccion.objects.get_or_create(direccionid=cliente[0]['direccionid'])
            perfil_direccion.calle = calle
            perfil_direccion.numero = numero
            perfil_direccion.comunaid = Comuna.objects.get(comunaid=comuna_id)
            perfil_direccion.tipoviviendaid = Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id)
            perfil_direccion.tipobarrioid = Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id)
            perfil_direccion.nombresector = nombre_sector
            perfil_direccion.save()

        if perfil_empresa is not None:
            
            perfil_empresa, created = Empresa.objects.get_or_create(empresaid=usuario[0]['empresaid'])
            perfil_empresa.razonsocial = razon_social
            perfil_empresa.rutcuerpo = rut_cuerpo
            perfil_empresa.dv = dv
            perfil_empresa.fono = fono
            perfil_empresa.save()

        perfil_usuario, created = Usuario.objects.get_or_create(personaid=persona[0]['personaid'])
        perfil_usuario.email = email
        perfil_usuario.save()
        
        user_django = User.objects.get(email=usuario[0]['email'])
        user_django.username = user_django.username
        user_django.first_name = nombres
        user_django.last_name = apellido_paterno
        user_django.email = email
        user_django.save()

        sweetify.success(request,"Perfil actualizado correctamente")
        return redirect('ver_perfil')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'clientes/editar_perfil.html', context)


def Registro_clientes(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'form3': form3,
        'tipo_usuario': tipo_usuario
    }

    return render(request, 'clientes/registro_clientes.html', context)


@login_required(login_url="ingreso")
def Agregar_cliente(request):
    
    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')
    
    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'form3': form3,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'clientes/agregar_cliente.html', context)


@login_required(login_url="ingreso")
def Listar_clientes(request):
    
    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'clientes':clientes,
        'tipo_usuario': tipo_usuario
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


@login_required(login_url="ingreso")
def Ver_cliente(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    old_post = request.session.get('_old_post')
    cliente = Cliente.objects.get(clienteid=old_post['VerCliente'])

    context = {
        'tipo_usuario': tipo_usuario,
        'cliente':cliente
    }

    return render(request, 'clientes/ver_cliente.html', context)

@login_required(login_url="ingreso")
def Editar_cliente(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'clientes/editar_cliente.html', context)

def Registro_clientes_empresa(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None
    
    form1 = FormClienteNormal1()
    form2 = FormClienteNormal2()
    form3 = FormClienteNormal3()
    form4 = FormClienteEmpresa()

    if request.method == 'POST':
        
        run_cuerpo = request.POST.get('runcuerpo')
        dv = request.POST.get('dv')
        rut_cuerpo = request.POST.get('rutcuerpo')
        dv_emp = request.POST.get('dv')
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
        razon_social = request.POST.get('razonsocial')
        fono = request.POST.get('fono')

        personaRegistro = Persona.objects.filter(runcuerpo=run_cuerpo, dv=dv).exists()
        usuarioRegistro = Usuario.objects.filter(email = email).exists()
        usuarioRegistro3 = Usuario.objects.filter(nombreusuario = nombre_usuario).exists()
        usuarioRegistroEmp = Empresa.objects.filter(razonsocial = razon_social).exists()

        if personaRegistro == True:
            sweetify.warning(request,"El run ingresado ya existe")
        elif usuarioRegistro == True:
            sweetify.warning(request,"El correo ingresado ya existe")
        elif usuarioRegistro3 == True:
            sweetify.warning(request,"El usuario ingresado ya esta registrado")
        elif usuarioRegistroEmp == True:
            sweetify.warning(request,"La razón social ingresada ya existe")
        else: 
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
            
            ValidarDireccion = Direccion.objects.filter(calle = calle, 
                numero = numero, 
                tipoviviendaid = tipo_vivienda_id).exists()

            if ValidarDireccion == False:

                Direccion.objects.create(
                    calle = calle,
                    numero = numero,
                    comunaid = Comuna.objects.get(comunaid=comuna_id),
                    tipoviviendaid = Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id),
                    tipobarrioid = Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id),
                    nombresector = nombre_sector
                )

            Empresa.objects.create(
                razonsocial = razon_social,
                rutcuerpo = rut_cuerpo,
                dv = dv_emp,
                fono = fono,
                estado = Estado.objects.get(descripcion="Activo")
            )

            Cliente.objects.create(
                direccionid = Direccion.objects.get(calle=calle, numero=numero),
                personaid = Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                empresaid = Empresa.objects.get(rutcuerpo=rut_cuerpo, dv=dv_emp),
                estadoid = Estado.objects.get(descripcion="Activo")
            )

            Usuario.objects.create(
                email = email,
                password = contraseña,
                personaid = Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                rolid = Rolusuario.objects.get(descripcion="Cliente"),
                nombreusuario = nombre_usuario
            )

            if (Persona is not None and 
                Direccion is not None and 
                Usuario is not None and 
                Cliente is not None and 
                user is not None):
                
                user.save()

                sweetify.success(request,"Se ha registrado correctamente")
                return redirect('index')
            else:
                sweetify.error(request,"No es posible registrarse en este momento")

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'clientes/registro_clientes_empresa.html', context)

##******************************************************************************************

##********************************Vendedores************************************************

@login_required(login_url="ingreso")
def Listar_vendedores(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'vendedores':vendedores,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'vendedores/listar_vendedores.html', context)

@login_required(login_url="ingreso")
def Agregar_vendedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'form3': form3,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'vendedores/agregar_vendedor.html', context)

@login_required(login_url="ingreso")
def Ver_vendedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    old_post = request.session.get('_old_post')
    vendedor = Empleado.objects.get(empleadoid=old_post['VerVendedor'])

    context = {
        'vendedor':vendedor,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'vendedores/ver_vendedor.html', context)

@login_required(login_url="ingreso")
def Editar_vendedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'form3': form3,
        'tipo_usuario': tipo_usuario,
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


def Listar_clientes_vendedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    clientes = Cliente.objects.all()

    if request.method == 'POST':

        if request.POST.get('VerCliente') is not None:
            request.session['_ver_cliente'] = request.POST
            return HttpResponseRedirect('ver_cliente_vendedor')

    context = {
        'tipo_usuario': tipo_usuario,
        'clientes': clientes,
    }

    return render(request, 'vendedores/listar_clientes_vendedor.html', context)


def Ver_cliente_vendedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    ver_cliente_post = request.session.get('_ver_cliente')

    ver_cliente = Persona.objects.filter(runcuerpo=ver_cliente_post['run'], dv=ver_cliente_post['dv']).values('personaid')
    cliente_id = Cliente.objects.filter(personaid=ver_cliente[0]['personaid']).values('clienteid')
    direccion = Direccioncliente.objects.filter(cliente_clienteid=cliente_id[0]['clienteid']).values('direccion_direccionid')
    direccion = Direccion.objects.get(direccionid=direccion[0]['direccion_direccionid'])
    cliente = Cliente.objects.get(personaid=ver_cliente[0]['personaid'])

    if request.method == 'POST':

        if request.POST.get('EditarCliente') is not None:
            request.session['_editar_cliente'] = request.POST
            return HttpResponseRedirect('editar_cliente_vendedor')

    context = {
        'tipo_usuario': tipo_usuario,
        'cliente': cliente,
        'direccion': direccion
    }

    return render(request, 'vendedores/ver_cliente_vendedor.html', context)

@login_required(login_url="ingreso")
def Agregar_cliente_vendedor(request):
    
    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')
    
    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        usuarioRegistro = Usuario.objects.filter(email = email).exists()
        usuarioRegistro3 = Usuario.objects.filter(nombreusuario = nombre_usuario).exists()

        if personaRegistro == True:
            sweetify.warning(request,"El run ingresado ya existe")
        elif usuarioRegistro == True:
            sweetify.warning(request,"El correo ingresado ya existe")
        elif usuarioRegistro3 == True:
            sweetify.warning(request,"El cliente ya cuenta con un usuario")
        else: 
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
            
            ValidarDireccion = Direccion.objects.filter(calle = calle, 
                numero = numero, 
                tipoviviendaid = tipo_vivienda_id).exists()

            if ValidarDireccion == False:

                Direccion.objects.create(
                    calle = calle,
                    numero = numero,
                    comunaid = Comuna.objects.get(comunaid=comuna_id),
                    tipoviviendaid = Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id),
                    tipobarrioid = Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id),
                    nombresector = nombre_sector
                )

            direccion = Direccion.objects.get(
                    calle = calle,
                    numero = numero,
                    comunaid = Comuna.objects.get(comunaid=comuna_id),
                    tipoviviendaid = Tipovivienda.objects.get(tipoviviendaid=tipo_vivienda_id),
                    tipobarrioid = Tipobarrio.objects.get(tipobarrioid=tipo_barrio_id),
                    nombresector = nombre_sector
                )

            Cliente.objects.create(
                personaid = Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                estadoid = Estado.objects.get(descripcion="Activo")
            )

            cliente = Cliente.objects.get(
                personaid = Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                estadoid = Estado.objects.get(descripcion="Activo")
            )

            Direccioncliente.objects.create(
                iddircliente = 2,
                direccion_direccionid = direccion,
                cliente_clienteid = cliente
            )

            Usuario.objects.create(
                email = email,
                password = contraseña,
                personaid = Persona.objects.get(runcuerpo=run_cuerpo, dv=dv),
                rolid = Rolusuario.objects.get(descripcion="Cliente"),
                nombreusuario = nombre_usuario
            )

            if (Persona is not None and 
                Direccion is not None and 
                Usuario is not None and 
                Cliente is not None and 
                user is not None):
                
                user.save()

                sweetify.success(request,"Cliente creado correctamente")
                return redirect('registro_clientes')
            else:
                sweetify.error(request,"No es posible crear el cliente en este momento")

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'vendedores/agregar_cliente_vendedor.html', context)


def Editar_cliente_vendedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    editar_cliente = request.session.get('_editar_cliente')
    
    cliente = Cliente.objects.filter(clienteid=editar_cliente['EditarCliente']).values('personaid')
    cliente_persona = Persona.objects.get(personaid=cliente[0]['personaid'])
    cliente_usuario = Usuario.objects.get(personaid=cliente[0]['personaid'])
    direccion1 = Direccioncliente.objects.filter(cliente_clienteid=editar_cliente['EditarCliente']).values('direccion_direccionid')
    direccion = Direccion.objects.get(direccionid=direccion1[0]['direccion_direccionid'])

    form1 = FormClienteNormal1(request.POST or None, instance=cliente_persona)
    form2 = FormClienteNormal2(request.POST or None, instance=direccion)
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

        cliente_persona, created = Persona.objects.get_or_create(personaid=cliente[0]['personaid'])
        cliente_persona.runcuerpo = run_cuerpo
        cliente_persona.dv = dv
        cliente_persona.apellidopaterno = apellido_paterno
        cliente_persona.apellidomaterno = apellido_materno
        cliente_persona.nombres = nombres
        cliente_persona.telefono = telefono
        cliente_persona.save()

        cliente_direccion, created = Direccion.objects.get_or_create(direccionid=direccion1[0]['direccion_direccionid'])
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

        sweetify.success(request,"Cliente actualizado correctamente")
        return redirect('ver_cliente_vendedor')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'vendedores/editar_cliente_vendedor.html', context)
##********************Proveedores*******************************************************************

@login_required(login_url="ingreso")
def Agregar_proveedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None
        
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
        'tipo_usuario': tipo_usuario,
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


@login_required(login_url="ingreso")
def Listar_proveedores(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'proveedor': proveedor,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'proveedores/listar_proveedores.html', context)


@login_required(login_url="ingreso")
def Ver_proveedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    old_post = request.session.get('_old_post')
    proveedor = Proveedor.objects.get(proveedorid=old_post['VerProveedor'])

    context = {
        'proveedor':proveedor,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'proveedores/ver_proveedor.html', context)


@login_required(login_url="ingreso")
def Editar_proveedor(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'proveedores/editar_proveedor.html', context)

# ********************************Empleados************************************************

@login_required(login_url="ingreso")
def Listar_empleados(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'empleados':empleados,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'empleados/listar_empleados.html', context)

@login_required(login_url="ingreso")
def Agregar_empleado(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'form3': form3,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'empleados/agregar_empleado.html', context)

@login_required(login_url="ingreso")
def Ver_empleado(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

    old_post = request.session.get('_old_post')
    empleado = Empleado.objects.get(empleadoid=old_post['VerEmpleado'])

    context = {
        'empleado':empleado,
        'tipo_usuario': tipo_usuario,
    }

    return render(request, 'empleados/ver_empleado.html', context)

@login_required(login_url="ingreso")
def Editar_empleado(request):

    if request.POST.get('VerPerfil') is not None:
        request.session['_ver_perfil'] = request.POST
        return redirect('ver_perfil')

    if Usuario.objects.filter(nombreusuario=request.user).exists():
        tipo_usuario = Usuario.objects.get(nombreusuario=request.user)
        tipo_usuario = tipo_usuario.rolid.descripcion
    else: 
        tipo_usuario = None

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
        'form3': form3,
        'tipo_usuario': tipo_usuario,
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
def Crear_pedido(request, id=None):
    proveedor = Proveedor.objects.get(proveedorid=id)
    listaProds = Productoproveedor.objects.filter(proveedorid=proveedor)
   
    # proveedor = Proveedor.objects.filter(proveedorid=id)
    # prod_prov = []
    # for prov in proveedor:
    #     productos = Productoproveedor.objects.filter(proveedorid=prov)
    #     for p in productos:
    #         prod_prov.append(p.productoid.productoid)
    #     productos = Producto.objects.filter(productoid__in=prod_prov)
    # listaProds = []
    # for prod in productos:
    #     listaProds.append(prod.nombre)

    if request.method == 'POST':
        lista_productos = []
        for key, value in request.POST.items():
            print(f"key: {key}  value  {value}")

            try:
                Producto.objects.get(productoid=key)
                if len(lista_productos) == 0:
                    lista_productos.append({'id': key, 'value': value})
                else:
                    for product in lista_productos:
                        if product['id'] == key:
                            sum_value = int(product['value']) + int(value)
                            product.update({'value': sum_value})
                        else:
                            lista_productos.append({'id': key, 'value': value})
                            break

            except Exception as error:
                if len(value) == 0:
                    fecha = "1000-10-10"
                else:
                    partes = value.split("/")
                    fecha = "-".join(reversed(partes))
        proveedor_orden = Proveedor.objects.get(proveedorid=int(id))
        estado_orden = Estadoorden.objects.get(estadoordenid=1)

        ordenPedido = Ordencompra.objects.create(
            fechapedido=fecha,
            proveedorid=proveedor_orden,
            estadoordenid=estado_orden
        )

        last_orden_compra = Ordencompra.objects.order_by('ordenid').last()
        estado_detalle = Estado.objects.get(estadoid=1)

        for products in lista_productos:
            producto = Producto.objects.get(productoid=int(products['id']))

            detallePedido = Detalleorden.objects.create(
                productoid=producto,
                cantidad=products['value'],
                ordenid=last_orden_compra,
                estadoid=estado_detalle

            )
        sweetify.success(request, "Orden de pedido realizada con exito")
        return redirect('listar_pedidos')

    context = {
        'listaProds': listaProds
    }
    return render(request, 'pedidos/crear_pedido.html', context)


def filtro_proveedor(request):
    proveedores = Proveedor.objects.all()
    context = {
        'proveedores': proveedores,
    }

    return render(request, 'pedidos/crear_pedido_proveedores.html', context)


def cambiar_estado_pedido(id_pedido):
    orden_compra = Ordencompra.objects.get(ordenid=int(id_pedido))
    detalle_orden = Detalleorden.objects.filter(ordenid=int(id_pedido))
    estado_eliminado = Estadoorden.objects.get(estadoordenid=23)
    estado_eliminado_detale = Estado.objects.get(estadoid=2)

    if orden_compra.estadoordenid.estadoordenid == 1:
        orden_compra.estadoordenid = estado_eliminado
        orden_compra.save()

    for detalle in detalle_orden:
        print(detalle)
        detalle.estadoid = estado_eliminado_detale
        detalle.save()


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
    detalle_orden = Detalleorden.objects.filter(ordenid=old_post['VerPedido'])
    recepcion_orden = Recepcion.objects.filter(ordenid=old_post['VerPedido'])

    context = {
        'detalle_orden': detalle_orden,
        'recepcion_orden':recepcion_orden
    }

    return render(request, 'pedidos/ver_pedido.html', context)


# ***************************Recepcionar pedidos*******************************************

def RecepcionPedido(request, id=None):
    if id:
        orden_pedido = Ordencompra.objects.filter(ordenid=id)
        detalle_orden = Detalleorden.objects.filter(ordenid=id, estadoid=1)
        productos = Producto.objects.all()

    if request.method == 'POST':
        for key, value in request.POST.items():
            print(f"key:{key} value:{value}")
            orden_pedido = Ordencompra.objects.get(ordenid=id)
            detalle_orden = Detalleorden.objects.filter(ordenid=orden_pedido)

            if key == "csrfmiddlewaretoken":
                pass
            else:
                try:
                    orden_pedido = Ordencompra.objects.get(ordenid=id)
                    producto_r = Producto.objects.get(productoid=key)
                    id_producto = producto_r.productoid
                    detalle = Detalleorden.objects.get(ordenid=id, productoid=id_producto)

                    Recepcion.objects.create(
                        fecharecepcion=datetime.datetime.now().date(),
                        cantidad=detalle.cantidad,
                        productoid=detalle.productoid,
                        proveedorid=orden_pedido.proveedorid,
                        ordenid=orden_pedido
                    )

                    detalle, created = Detalleorden.objects.get_or_create(ordenid=id, productoid=id_producto)
                    detalle.estadoid = Estado.objects.get(estadoid=2)
                    detalle.save()

                    producto_recepcionar, created = Producto.objects.get_or_create(productoid=id_producto)
                    producto_recepcionar.stock = producto_recepcionar.stock + detalle.cantidad
                    producto_recepcionar.save()
                    sweetify.success(request, "Productos recepcionados satisfactoriamente")
                except Exception as error:
                    sweetify.warning(request, "No es posible Recepcionar el producto en este momento")
                    print(error)

        verificar_detalle_orden = Detalleorden.objects.filter(ordenid=id, estadoid=1)
        if len(verificar_detalle_orden) == 0:
            orden, created = Ordencompra.objects.get_or_create(ordenid=id)
            orden.estadoordenid = Estadoorden.objects.get(estadoordenid=22)
            orden.save()
        else:
            orden, created = Ordencompra.objects.get_or_create(ordenid=id)
            orden.estadoordenid = Estadoorden.objects.get(estadoordenid=41)
            orden.save()

        return redirect('listar_pedidos')

    context = {
        'ordenPedido': orden_pedido,
        'productos': productos,
        'detalleOrden': detalle_orden,
    }

    return render(request, 'recepcion_pedido.html', context)

@login_required(login_url="ingreso")
def crear_venta(request):
    productos = Productoproveedor.objects.all()
    form = FormCliente()
    form_doc = FormVenta()

    total = 0
    if request.method == 'POST':
        productos_venta = []
        for key, value in request.POST.items():
            print(f"key: {key}  value  {value}")
            if key == "csrfmiddlewaretoken":
                pass
            elif key == "clienteid":
                cliente_venta = Cliente.objects.get(clienteid=value)
            elif key == "tipodocumentoid":
                documento_venta = Tipodocumento.objects.get(tipodocumentoid=value)
            else:
                try:
                    key = int(key)
                    try:
                        producto = Producto.objects.get(productoid=int(key))
                    except Producto.DoesNotExist:
                        sweetify.warning(request, "Ocurrio un Problema")
                        print(error)
                        return render(request, 'index.html')
                except Exception as error:
                    if "cantidad" in key:
                        cantidad = value

                    elif key != "total" and "total" in key:
                        total = value.replace("$", "")
                        productos_venta.append([producto, cantidad, total])
                    elif key == "total":
                        total_venta = value

        Venta.objects.create(
            fechaventa=datetime.datetime.now().date(),
            totalventa=total_venta,
            tipodocumentoid=documento_venta,
            clienteid=cliente_venta,
            tipopagoid=0
        )

        ultima_ventas = Venta.objects.order_by('nroventa').last()
        for producto in productos_venta:
            Detalleventa.objects.create(
                cantidad = producto[1],
                subtotal = int(producto[2]) * int(producto[1]),
                productoid = producto[0],
                nroventa = ultima_ventas
            )
            producto_modificar = producto[0]
            producto_vendido, created = Producto.objects.get_or_create(productoid=producto_modificar.productoid)
            producto_vendido.stock = producto_vendido.stock-int(producto[1])
            producto_vendido.save()

    
        if documento_venta.tipodocumentoid in [2,4]:
            Factura.objects.create(
                fechafactura = datetime.datetime.now().date(),
                neto = int(total_venta)-(int(total_venta)*0.19),
                iva = int(total_venta)*0.19,
                totalfactura = total_venta,
                nroventa = ultima_ventas,
                estadoid = Estado.objects.get(descripcion="Activo")
            )
          
        elif documento_venta.tipodocumentoid in [1,3]:
            Boleta.objects.create(
                fechaboleta = datetime.datetime.now().date(),
                totalboleta = total_venta,
                nroventa = ultima_ventas,
                estadoid = Estado.objects.get(descripcion="Activo")
            )

        messages.warning(request, 'Venta realizada con exito')
        return redirect('crear_venta')


    return render(request, 'ventas/crear_venta.html',{'productos':productos, 'form':form, 'form_doc':form_doc})


def listar_ventas(request):
    ventas = Venta.objects.all()

    if request.method == 'POST':
        # if request.POST.get('CambiarEstado') is not None:
        #     id_pedido = request.POST.get('CambiarEstado')
        #     print(id_pedido)
        #     cambiar_estado_pedido(id_pedido)
        #     orden_compra = Ordencompra.objects.get(ordenid=id_pedido)
        #     sweetify.success(request,
        #                      f'La Nro:{orden_compra.ordenid} se elimino correctamente')
        #     return redirect('listar_pedidos')

        if request.POST.get('VerVenta') is not None:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect('ver_venta')

    context = {
        'ventas': ventas
    }

    return render(request, 'ventas/listar_ventas.html', context)


def ver_venta(request):
    old_post = request.session.get('_old_post')
    detalle_venta = Detalleventa.objects.filter(nroventa=old_post['VerVenta'])
    ventas = Venta.objects.filter(nroventa=old_post['VerVenta'])

    context = {
        'detalle_venta': detalle_venta,
        'ventas': ventas
    }

    return render(request, 'ventas/ver_venta.html', context)

