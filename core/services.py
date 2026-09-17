from decimal import Decimal
from .models import Comprobante, DatosFacturacion, JornadaComercial

class GeneradorVentasService:
    @staticmethod
    def calcular_totales(subtotal_neto):
        """Calcula el 19% de IVA y el total general de forma centralizada."""
        tasa_iva = Decimal('0.19') # 19% de IVA exigido tributariamente
        monto_iva = subtotal_neto * tasa_iva
        total_general = subtotal_neto + monto_iva
        
        return {
            'subtotal_neto': round(subtotal_neto, 2),
            'monto_iva': round(monto_iva, 2),
            'total_general': round(total_general, 2)
        }

    @staticmethod
    def validar_jornada(jefe_apertura):
        """Verifica o crea la jornada comercial actual."""
        from datetime import date
        hoy = date.today()
        jornada, created = JornadaComercial.objects.get_or_create(
            fecha=hoy,
            defaults={'estado': 'ABIERTO', 'id_jefe_apertura': jefe_apertura}
        )
        return jornada

class ComprobanteFactory:
    """Patrón Factory: Creación dinámica desacoplada de Boletas y Facturas."""
    @staticmethod
    def crear_documento(venta, tipo_documento, datos_factura=None):
        # Generar un número de documento ficticio basado en el ID de la venta
        prefijo = "FAC" if tipo_documento == 'FACTURA' else "BOL"
        numero_doc = f"{prefijo}-100{venta.id}"

        # Se instancia el comprobante
        comprobante = Comprobante.objects.create(
            id_venta=venta,
            tipo_documento=tipo_documento,
            numero_documento=numero_doc,
            base_neta=venta.subtotal_neto,
            iva=venta.monto_iva
        )

        # Si el tipo es Factura, es obligatorio guardar la información tributaria
        if tipo_documento == 'FACTURA' and datos_factura:
            DatosFacturacion.objects.create(
                id_comprobante=comprobante,
                rut=datos_factura.get('rut', ''),
                razon_social=datos_factura.get('razon_social', ''),
                giro=datos_factura.get('giro', ''),
                direccion=datos_factura.get('direccion', '')
            )
        
        return comprobante