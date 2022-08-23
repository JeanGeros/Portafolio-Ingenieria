from django.shortcuts import render
from src.forms import (
    FormClienteNormal1, FormClienteNormal2, FormClienteNormal3, addproductsForm
)
<<<<<<< HEAD
=======
from .models import Persona, Direccion, Usuario
>>>>>>> master

def Index(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def addProducts(request):
    data = {
        'form': addproductsForm()
    }

    if request.method == 'POST':
        formulario = addproductsForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.saves()
            data["mensaje"] = "Guardado Correctamente"
        else:
            data["form"] = formulario
    return render(request, 'Modulo_productos/addProducts.html', data)

def listar_productos(request):
    return render(request, 'Modulo_productos/listarProductos.html')

def Registro_clientes(request):

    form1 = FormClienteNormal1()
    form2 = FormClienteNormal2()
    form3 = FormClienteNormal3()

    if request.method == 'POST':

        run_cuerpo = request.POST.get('run_cuerpo')
        dv = request.POST.get('dv')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        calle = request.POST.get('calle')
        numero = request.POST.get('numero')
        comuna_id = request.POST.get('comuna_id')
        tipo_vivienda_id = request.POST.get('tipo_vivienda_id')
        tipo_barrio_id = request.POST.get('tipo_barrio_id')
        nombre_sector = request.POST.get('nombre_sector')
        contraseña = request.POST.get('contraseña')

        # Estado activo = 1 e inactivo = 2 
        persona = Persona.objects.create(
            runcuerpo = run_cuerpo,
            dv = dv,
            apellidopaterno = apellido_paterno,
            apellidomaterno = apellido_materno,
            nombres = nombres,
            telefono = telefono,
            estadoid = 1
        )
        persona.save()

        direccion = Direccion.objects.create(
            calle = calle,
            numero = numero,
            comunaid = comuna_id,
            tipoviviendaid = tipo_vivienda_id,
            tipobarrioid = tipo_barrio_id,
            nombresector = nombre_sector
        )
        direccion.save()

        usuario = Usuario.objects.create(
            email = email,
            password = contraseña,
            rol = 4
        )
        usuario.save()

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'usuarios/registro_clientes.html', context)