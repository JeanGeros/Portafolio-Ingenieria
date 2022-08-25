from django import forms
from .models import Producto, Persona, Direccion, Usuario

class FormClienteNormal1(forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = ("runcuerpo", "dv", "apellidopaterno", "apellidomaterno", "nombres", "telefono")

class FormClienteNormal2(forms.ModelForm):
    
    class Meta:
        model = Direccion
        fields = ("calle", "numero", "comunaid", "tipoviviendaid", "tipobarrioid",)

class FormClienteNormal3(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ("email","password")

class addproductsForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

