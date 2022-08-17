from django.db import models


class Accionpagina(models.Model):
    accionid = models.BigIntegerField(primary_key=True)
    fechain = models.DateField()
    modulo = models.CharField(max_length=100)
    usuarioid = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuarioid')

    class Meta:
        managed = False
        db_table = 'accionpagina'


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


class Boleta(models.Model):
    boletaid = models.BigIntegerField(primary_key=True)
    nroboleta = models.BigIntegerField()
    totalboleta = models.BigIntegerField()
    ventaid = models.ForeignKey('Venta', models.DO_NOTHING, db_column='ventaid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boleta'


class Cliente(models.Model):
    clienteid = models.BigIntegerField(primary_key=True)
    direccionid = models.ForeignKey('Direccion', models.DO_NOTHING, db_column='direccionid')
    personaid = models.ForeignKey('Persona', models.DO_NOTHING, db_column='personaid', blank=True, null=True)
    empresaid = models.ForeignKey('Empresa', models.DO_NOTHING, db_column='empresaid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Comuna(models.Model):
    comunaid = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=25)
    regionid = models.ForeignKey('Region', models.DO_NOTHING, db_column='regionid')

    class Meta:
        managed = False
        db_table = 'comuna'


class Detallepedido(models.Model):
    detalleid = models.BigIntegerField(primary_key=True)
    cantidad = models.BigIntegerField()
    productoid = models.ForeignKey('Producto', models.DO_NOTHING, db_column='productoid')
    pedidoid = models.ForeignKey('Pedido', models.DO_NOTHING, db_column='pedidoid')

    class Meta:
        managed = False
        db_table = 'detallepedido'


class Direccion(models.Model):
    direccionid = models.BigIntegerField(primary_key=True)
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=10)
    comunaid = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='comunaid')
    tipoviviendaid = models.ForeignKey('Tipovivienda', models.DO_NOTHING, db_column='tipoviviendaid')
    tipobarrioid = models.ForeignKey('Tipobarrio', models.DO_NOTHING, db_column='tipobarrioid')

    class Meta:
        managed = False
        db_table = 'direccion'


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
    cargo = models.CharField(max_length=25)
    funcion = models.CharField(max_length=25, blank=True, null=True)
    personaid = models.ForeignKey('Persona', models.DO_NOTHING, db_column='personaid')

    class Meta:
        managed = False
        db_table = 'empleado'


class Empresa(models.Model):
    empresaid = models.BigIntegerField(primary_key=True)
    razonsocial = models.CharField(max_length=50)
    rutcuerpo = models.BigIntegerField()
    dv = models.CharField(max_length=1)
    fono = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresa'


class Factura(models.Model):
    facturaid = models.BigIntegerField(primary_key=True)
    nrofactura = models.BigIntegerField()
    neto = models.BigIntegerField()
    iva = models.BigIntegerField()
    totalfactura = models.BigIntegerField()
    ventaid = models.ForeignKey('Venta', models.DO_NOTHING, db_column='ventaid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factura'


class Familiaproducto(models.Model):
    familiaproid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'familiaproducto'


class Guiadespacho(models.Model):
    guiaid = models.BigIntegerField(primary_key=True)
    nroguia = models.BigIntegerField()
    ventaid = models.ForeignKey('Venta', models.DO_NOTHING, db_column='ventaid')
    clienteid = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='clienteid')

    class Meta:
        managed = False
        db_table = 'guiadespacho'


class Notacredito(models.Model):
    notaid = models.BigIntegerField(primary_key=True)
    numero = models.BigIntegerField()
    total = models.BigIntegerField()
    facturaid = models.ForeignKey(Factura, models.DO_NOTHING, db_column='facturaid')

    class Meta:
        managed = False
        db_table = 'notacredito'


class Pedido(models.Model):
    pedidoid = models.BigIntegerField(primary_key=True)
    fechapedido = models.DateField()
    proveedorid = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedorid')

    class Meta:
        managed = False
        db_table = 'pedido'


class Persona(models.Model):
    personaid = models.BigIntegerField(primary_key=True)
    runcuerpo = models.BigIntegerField()
    dv = models.CharField(max_length=1)
    apellidopaterno = models.CharField(max_length=25)
    apellidomaterno = models.CharField(max_length=25)
    nombres = models.CharField(max_length=50)
    telefono = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persona'


class Producto(models.Model):
    productoid = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = models.BigIntegerField()
    stock = models.BigIntegerField()
    stockcritico = models.BigIntegerField()
    fechavencimiento = models.DateField()
    codigo = models.CharField(max_length=17)
    imagen = models.CharField(max_length=256, blank=True, null=True)
    proveedorid = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedorid')
    tipoproductoid = models.ForeignKey('Tipoproducto', models.DO_NOTHING, db_column='tipoproductoid')
    familiaproid = models.ForeignKey(Familiaproducto, models.DO_NOTHING, db_column='familiaproid')

    class Meta:
        managed = False
        db_table = 'producto'


class Proveedor(models.Model):
    proveedorid = models.BigIntegerField(primary_key=True)
    razonsocial = models.CharField(max_length=50)
    rut = models.CharField(max_length=11)
    fono = models.BigIntegerField(blank=True, null=True)
    rubroid = models.ForeignKey('Tiporubro', models.DO_NOTHING, db_column='rubroid')
    direccionid = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='direccionid')

    class Meta:
        managed = False
        db_table = 'proveedor'


class Recepcion(models.Model):
    recepcionid = models.BigIntegerField(primary_key=True)
    fecharecepcion = models.DateField()
    cantidad = models.BigIntegerField()
    pedidoid = models.ForeignKey(Pedido, models.DO_NOTHING, db_column='pedidoid')
    proveedorid = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='proveedorid')
    productoid = models.ForeignKey(Producto, models.DO_NOTHING, db_column='productoid')

    class Meta:
        managed = False
        db_table = 'recepcion'


class Region(models.Model):
    regionid = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'region'


class Rolusuario(models.Model):
    rolid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'rolusuario'


class Tipobarrio(models.Model):
    tipobarrioid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'tipobarrio'


class Tipodocumento(models.Model):
    tipoid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'tipodocumento'


class Tipoproducto(models.Model):
    tipoproductoid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipoproducto'


class Tiporubro(models.Model):
    rubroid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tiporubro'


class Tipovivienda(models.Model):
    tipoviviendaid = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'tipovivienda'


class Usuario(models.Model):
    usuarioid = models.BigIntegerField(primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    rolid = models.ForeignKey(Rolusuario, models.DO_NOTHING, db_column='rolid')
    personaid = models.ForeignKey(Persona, models.DO_NOTHING, db_column='personaid', blank=True, null=True)
    empresaid = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='empresaid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Venta(models.Model):
    ventaid = models.BigIntegerField(primary_key=True)
    nroventa = models.BigIntegerField()
    cantidad = models.BigIntegerField()
    totalventa = models.BigIntegerField()
    clienteid = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='clienteid')
    productoid = models.ForeignKey(Producto, models.DO_NOTHING, db_column='productoid')
    tipodocid = models.ForeignKey(Tipodocumento, models.DO_NOTHING, db_column='tipodocid')

    class Meta:
        managed = False
        db_table = 'venta'
