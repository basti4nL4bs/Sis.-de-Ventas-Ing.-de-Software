from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('VENDEDOR', 'Vendedor'),
        ('JEFE_VENTAS', 'Jefe de Ventas'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='VENDEDOR')

class JornadaComercial(models.Model):
    ESTADOS = (
        ('ABIERTO', 'Abierto'),
        ('CERRADO', 'Cerrado'),
    )
    fecha = models.DateField(unique=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ABIERTO')
    id_jefe_apertura = models.ForeignKey(Usuario, on_delete=models.RESTRICT)

class Producto(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=150)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class Venta(models.Model):
    id_vendedor = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    id_jornada = models.ForeignKey(JornadaComercial, on_delete=models.RESTRICT)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    subtotal_neto = models.DecimalField(max_digits=10, decimal_places=2)
    monto_iva = models.DecimalField(max_digits=10, decimal_places=2)
    total_general = models.DecimalField(max_digits=10, decimal_places=2)

class DetalleVenta(models.Model):
    id_venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    codigo_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class Comprobante(models.Model):
    TIPOS = (
        ('BOLETA', 'Boleta'),
        ('FACTURA', 'Factura'),
    )
    id_venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=10, choices=TIPOS)
    numero_documento = models.CharField(max_length=30, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    base_neta = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)

class DatosFacturacion(models.Model):
    id_comprobante = models.OneToOneField(Comprobante, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12)
    razon_social = models.CharField(max_length=150)
    giro = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)