from django import forms
from .models import Persona, Direccion, Usuario

class FormClienteNormal1(forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = ("runcuerpo","dv","apellidopaterno","apellidomaterno","nombres","telefono")

class FormClienteNormal2(forms.ModelForm):
    
    class Meta:
        model = Direccion
        fields = ("calle","numero","comunaid","tipoviviendaid","tipobarrioid","nombresector")

class FormClienteNormal3(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ("email","password")