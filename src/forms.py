from django import forms
from .models import Producto, Persona, Direccion, Usuario, Cliente

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

