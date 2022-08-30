from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, Persona, Direccion, Usuario, Cliente

class FormRegistroUsuario(UserCreationForm):

    class Meta:
        model = User
        fields = ("email","password1","password2")

class FormClienteNormal1(forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = ("runcuerpo", "dv", "apellidopaterno", "apellidomaterno", "nombres", "telefono")

class FormClienteNormal2(forms.ModelForm):
    
    class Meta:
        model = Direccion
        fields = ("calle", "numero", "comunaid", "tipoviviendaid", "tipobarrioid","nombresector")

class FormClienteNormal3(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ("email","password")

class FormEditarCliente(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs) 
    #     for field in iter(self.fields):  
    #         self.fields[field].widget.attrs.update({  
    #             'class': 'confirmar_contraseña'  
    #         })  

    class Meta:
        model = Cliente
        fields = ("direccionid","personaid","empresaid")

class addproductsForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

