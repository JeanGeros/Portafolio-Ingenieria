from django.shortcuts import render
from django import forms
from src.forms import (
    FormClienteNormal1, FormClienteNormal2, FormClienteNormal3, 
)


def Index(request):

    return render(request, 'index.html')

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
