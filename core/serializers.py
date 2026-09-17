from rest_framework import serializers
from .models import Producto, Venta, DetalleVenta, Comprobante, DatosFacturacion, JornadaComercial

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class JornadaComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = JornadaComercial
        fields = '__all__'

class DatosFacturacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosFacturacion
        fields = ['rut', 'razon_social', 'giro', 'direccion']

class ComprobanteSerializer(serializers.ModelSerializer):
    datos_facturacion = DatosFacturacionSerializer(source='datosfacturacion', read_only=True)
    
    class Meta:
        model = Comprobante
        fields = ['id', 'tipo_documento', 'numero_documento', 'fecha_emision', 'base_neta', 'iva', 'datos_facturacion']