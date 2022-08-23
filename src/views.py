from django.shortcuts import render
from src.forms import (
    FormClienteNormal1, FormClienteNormal2, FormClienteNormal3, addproductsForm
)

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

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }

    return render(request, 'usuarios/registro_clientes.html', context)