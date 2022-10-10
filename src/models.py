from django.db import models


class Accionpagina(models.Model):
    accionid = models.BigIntegerField(primary_key=True)
    fechain = models.DateField()
    modulo = models.CharField(max_length=100)
    fechaout = models.DateField(blank=True, null=True)
    usuarioid = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuarioid')

    def __str__(self):
        return self.modulo

    class Meta:
        managed = False
        db_table = 'accionpagina'


class Auditoria(models.Model):
    id = models.BigIntegerField(primary_key=True)
    menu = models.CharField(max_length=200)
    accion = models.CharField(max_length=250)
    usuario = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'auditoria'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bodega(models.Model):
    BodegaId = models.BigIntegerField(primary_key=True)
    pasillo = models.CharField(max_length=6)
    estante = models.CharField(max_length=6)
    casillero = models.CharField(max_length=6)

    def __str__(self):
        return f"Pasillo:{self.pasillo} Estante:{self.estante} casillero:{self.casillero}"

    class Meta:
        managed = False
        db_table = 'bodega'


class Boleta(models.Model):
    nroboleta = models.BigIntegerField(primary_key=True)
    fechaboleta = models.DateField()
    totalboleta = models.BigIntegerField()
    nroventa = models.ForeignKey('Venta', models.DO_NOTHING, db_column='nroventa')
    estadoid = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estadoid')

    def __str__(self):
        return self.nroboleta

    class Meta:
        managed = False
        db_table = 'boleta'


class Cargo(models.Model):
    cargoid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'cargo'


class Cliente(models.Model):
    clienteid = models.BigIntegerField(primary_key=True)
    personaid = models.ForeignKey('Persona', models.DO_NOTHING, db_column='personaid', blank=True, null=True)
    empresaid = models.ForeignKey('Empresa', models.DO_NOTHING, db_column='empresaid', blank=True, null=True)
    estadoid = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estadoid')

    class Meta:
        managed = False
        db_table = 'cliente'


class Comuna(models.Model):
    comunaid = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=25)
    regionid = models.ForeignKey('Region', models.DO_NOTHING, db_column='regionid')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'comuna'


class Despacho(models.Model):
    despachoid = models.BigIntegerField(primary_key=True)
    fechasolicitud = models.DateField()
    fechadespacho = models.DateField(blank=True, null=True)
    nroguia = models.ForeignKey('Guiadespacho', models.DO_NOTHING, db_column='nroguia')

    class Meta:
        managed = False
        db_table = 'despacho'


class Detalleorden(models.Model):
    detalleid = models.BigIntegerField(primary_key=True)
    cantidad = models.BigIntegerField()
    ordenid = models.ForeignKey('Ordencompra', models.DO_NOTHING, db_column='ordenid')
    productoid = models.ForeignKey('Producto', models.DO_NOTHING, db_column='productoid')
    estadoid = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estadoid', blank=True, null=True)

    def __str__(self):
        return f"id: {self.detalleid} id_order: {self.ordenid}"

    class Meta:
        managed = False
        db_table = 'detalleorden'


class Direccion(models.Model):
    direccionid = models.BigIntegerField(primary_key=True)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=10)
    nombresector = models.CharField(max_length=100)
    tipoviviendaid = models.ForeignKey('Tipovivienda', models.DO_NOTHING, db_column='tipoviviendaid')
    tipobarrioid = models.ForeignKey('Tipobarrio', models.DO_NOTHING, db_column='tipobarrioid')
    comunaid = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='comunaid')

    def __str__(self):
        return f"{self.calle} {self.numero}"

    class Meta:
        managed = False
        db_table = 'direccion'


class Direccioncliente(models.Model):
    id = models.BigIntegerField(primary_key=True)
    direccion_direccionid = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='direccion_direccionid')
    cliente_clienteid = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_clienteid')

    class Meta:
        managed = False
        db_table = 'direccioncliente'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empleado(models.Model):
    empleadoid = models.BigIntegerField(primary_key=True)
    fechaingreso = models.DateField()
    fechadesvinculacion = models.DateField(blank=True, null=True)
    personaid = models.ForeignKey('Persona', models.DO_NOTHING, db_column='personaid')
    cargoid = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='cargoid')
    estadoid = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estadoid')

    class Meta:
        managed = False
        db_table = 'empleado'


class Empresa(models.Model):
    empresaid = models.BigIntegerField(primary_key=True)
    razonsocial = models.CharField(max_length=50)
    rutcuerpo = models.BigIntegerField()
    dv = models.CharField(max_length=1)
    fono = models.BigIntegerField(blank=True, null=True)
    estadoid = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estadoid')

    def __str__(self):
        return self.razonsocial

    class Meta:
        managed = False
        db_table = 'empresa'


class Error(models.Model):
    id = models.BigIntegerField(primary_key=True)
    rutina = models.CharField(max_length=150)
    mensaje = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'error'


class Estado(models.Model):
    estadoid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=10)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'estado'


class Estadoorden(models.Model):
    estadoordenid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'estadoorden'


class Factura(models.Model):
    numerofactura = models.BigIntegerField(primary_key=True)
    fechafactura = models.DateField()
    neto = models.BigIntegerField()
    iva = models.BigIntegerField()
    totalfactura = models.BigIntegerField()
    nroventa = models.ForeignKey('Venta', models.DO_NOTHING, db_column='nroventa')
    estadoid = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estadoid')

    class Meta:
        managed = False
        db_table = 'factura'


class Familiaproducto(models.Model):
    familiaproid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'familiaproducto'


class Guiadespacho(models.Model):
    nroguia = models.BigIntegerField(primary_key=True)
    fechaguia = models.DateField()
    nroventa = models.ForeignKey('Venta', models.DO_NOTHING, db_column='nroventa')
    estadoid = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estadoid')

    class Meta:
        managed = False
        db_table = 'guiadespacho'


class Notacredito(models.Model):
    nronota = models.BigIntegerField(primary_key=True)
    fechanota = models.DateField()
    total = models.BigIntegerField()
    numerofactura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='numerofactura')
    estadoid = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estadoid')

    def __str__(self):
        return self.numero

    class Meta:
        managed = False
        db_table = 'notacredito'


class Ordencompra(models.Model):
    ordenid = models.BigIntegerField(primary_key=True)
    fechapedido = models.DateField()
    estadoordenid = models.ForeignKey(Estadoorden, models.DO_NOTHING, db_column='estadoordenid')
    proveedorid = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedorid')

    def __str__(self):
        return f"id: {self.ordenid} estado: {self.estadoordenid.descripcion}"

    class Meta:
        managed = False
        db_table = 'ordencompra'


class Persona(models.Model):
    personaid = models.BigIntegerField(primary_key=True)
    runcuerpo = models.BigIntegerField()
    dv = models.CharField(max_length=1)
    apellidopaterno = models.CharField(max_length=25)
    apellidomaterno = models.CharField(max_length=25)
    nombres = models.CharField(max_length=50)
    telefono = models.BigIntegerField(blank=True, null=True)
    estadoid = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estadoid')

    def __str__(self):
        return self.nombres

    class Meta:
        managed = False
        db_table = 'persona'


class Producto(models.Model):
    productoid = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = models.BigIntegerField()
    stock = models.BigIntegerField()
    stockcritico = models.BigIntegerField()
    fechavencimiento = models.DateField(blank=True, null=True)
    codigo = models.CharField(max_length=17)
    familiaproid = models.ForeignKey(Familiaproducto, models.DO_NOTHING, db_column='familiaproid')
    tipoproductoid = models.ForeignKey('Tipoproducto', models.DO_NOTHING, db_column='tipoproductoid')
    estadoid = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estadoid')
    imagen = models.ImageField(blank=True, null=True, upload_to="productos")
    BodegaId = models.ForeignKey(Bodega, models.DO_NOTHING, db_column='BodegaId')

    


    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'producto'


class Productoproveedor(models.Model):
    ProId = models.BigIntegerField(primary_key=True)
    productoid = models.ForeignKey(Producto, models.DO_NOTHING, db_column='productoid')
    proveedorid = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedorid')

    def __str__(self):
        return f"{self.productoid} {self.proveedorid}"

    class Meta:
        managed = False
        db_table = 'productoproveedor'


class Proveedor(models.Model):
    proveedorid = models.BigIntegerField(primary_key=True)
    razonsocial = models.CharField(max_length=50)
    rutcuerpo = models.BigIntegerField()
    dv = models.CharField(max_length=1)
    fono = models.BigIntegerField(blank=True, null=True)
    rubroid = models.ForeignKey('Tiporubro', models.DO_NOTHING, db_column='rubroid')
    direccionid = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='direccionid')
    estadoid = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estadoid')

    def __str__(self):
        return self.razonsocial

    class Meta:
        managed = False
        db_table = 'proveedor'


class Recepcion(models.Model):
    recepcionid = models.BigIntegerField(primary_key=True)
    fecharecepcion = models.DateField()
    cantidad = models.BigIntegerField()
    productoid = models.ForeignKey(Producto, models.DO_NOTHING, db_column='productoid')
    proveedorid = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='proveedorid')
    ordenid = models.ForeignKey(Ordencompra, models.DO_NOTHING, db_column='ordenid')

    class Meta:
        managed = False
        db_table = 'recepcion'


class Region(models.Model):
    regionid = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'region'


class Rolusuario(models.Model):
    rolid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=25)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'rolusuario'


class Tipobarrio(models.Model):
    tipobarrioid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=12)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'tipobarrio'


class Tipodocumento(models.Model):
    tipodocumentoid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=15)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'tipodocumento'


class Tipoproducto(models.Model):
    tipoproductoid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'tipoproducto'


class Tiporubro(models.Model):
    rubroid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'tiporubro'


class Tipovivienda(models.Model):
    tipoviviendaid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=12)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'tipovivienda'


class Usuario(models.Model):
    usuarioid = models.BigIntegerField(primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    nombreusuario = models.CharField(max_length=50)
    empresaid = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='empresaid', blank=True, null=True)
    personaid = models.ForeignKey(Persona, models.DO_NOTHING, db_column='personaid', blank=True, null=True)
    rolid = models.ForeignKey(Rolusuario, models.DO_NOTHING, db_column='rolid')

    def __str__(self):
        return self.email

    class Meta:
        managed = False
        db_table = 'usuario'


class Venta(models.Model):
    nroventa = models.BigIntegerField(primary_key=True)
    cantidad = models.BigIntegerField()
    fechaventa = models.DateField()
    totalventa = models.BigIntegerField()
    productoid = models.ForeignKey(Producto, models.DO_NOTHING, db_column='productoid')
    tipodocumentoid = models.ForeignKey(Tipodocumento, models.DO_NOTHING, db_column='tipodocumentoid')
    clienteid = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='clienteid')

    class Meta:
        managed = False
        db_table = 'venta'


class Ventadiaria(models.Model):
    id = models.BigIntegerField(primary_key=True)
    fecha = models.DateField()
    totalventa = models.BigIntegerField()
    tipodocumentoid = models.ForeignKey(Tipodocumento, models.DO_NOTHING, db_column='tipodocumentoid')
    nroventa = models.ForeignKey(Venta, models.DO_NOTHING, db_column='nroventa')

    class Meta:
        managed = False
        db_table = 'ventadiaria'
