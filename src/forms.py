
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Producto, Persona, Direccion, Proveedor, Usuario, Cliente, Empleado, Productoproveedor, Bodega, Empresa, Tipodocumento, Venta, Familiaproducto, Detalleorden,Estadoorden, Ordencompra

class FormRegistroUsuario(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "username","password1","password2")

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
        fields = ("email","password", "nombreusuario")

class FormClienteEmpresa(forms.ModelForm):
    
    class Meta:
        model = Empresa
        fields = ("razonsocial","rutcuerpo","dv","fono")

class FormEditarCliente(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'confirmar_contraseña'
    #         })

    class Meta:
        model = Cliente
        fields = ("personaid","empresaid")

class addproductsForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class FormProveedor(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

class FormProveedorUsuario(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ("email", "nombreusuario","password")

class FormDireProvee(forms.ModelForm):

    class Meta:
        model = Direccion
        fields = ("calle", "numero", "comunaid", "tipoviviendaid", "tipobarrioid","nombresector")

class FormVendedorPersona(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ("runcuerpo", "dv", "apellidopaterno", "apellidomaterno", "nombres", "telefono")

class FormVendedorUsuario(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ("email", "nombreusuario","password")

class FormVendedorEmpleado(forms.ModelForm):

    class Meta:
        model = Empleado
        fields = ("fechaingreso",)

class FormEmpleadoPersona(forms.ModelForm):

    class Meta:
        model = Persona
        fields = ("runcuerpo", "dv", "apellidopaterno", "apellidomaterno", "nombres", "telefono")

class FormEmpleadoUsuario(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ("email", "nombreusuario","password")

class FormEmpleadoEmpleado(forms.ModelForm):

    class Meta:
        model = Empleado
        fields = ("fechaingreso",)


class FormProductoproveedor(forms.ModelForm):
    class Meta:
        model = Productoproveedor
        fields = '__all__'
    


class FormBodega(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
    
class FormTipodocumento(forms.ModelForm):
    class Meta:
        model = Tipodocumento
        fields = '__all__'

class FormVenta(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

class FormDocu(forms.Form):
    opciones_documentos =(
        ("", "----------"),
        ("1", "Boleta Afecta"),
        ("2", "Factura Afecta"),
        ("3", "Boleta Exenta"),
        ("4", "Factura Exenta"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control'  
            })  

    Tipo_documento= forms.ChoiceField(choices = opciones_documentos)


class FormFamiliaProduct(forms.ModelForm):
    class Meta:
        model = Familiaproducto
        fields = '__all__'

class FormDetalleorden(forms.ModelForm):
    class Meta:
        model = Detalleorden
        fields = '__all__'

class FormEstadoorden(forms.ModelForm):
    class Meta:
        model = Ordencompra
        fields = '__all__'    

        