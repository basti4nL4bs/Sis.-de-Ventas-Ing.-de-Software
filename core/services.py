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

        # Validación estricta de datos fiscales obligatorios para Factura (OWASP e ISO 27000)
        if tipo_documento == 'FACTURA':
            campos_requeridos = ['rut', 'razon_social', 'giro', 'direccion']
            if not datos_factura or not all(str(datos_factura.get(c, '')).strip() for c in campos_requeridos):
                raise ValueError("Para comprobantes de tipo Factura, todos los datos tributarios son obligatorios.")

        # Se instancia el comprobante
        comprobante = Comprobante.objects.create(
            id_venta=venta,
            tipo_documento=tipo_documento,
            numero_documento=numero_doc,
            base_neta=venta.subtotal_neto,
            iva=venta.monto_iva
        )

        # Si es Factura, se persisten los datos tributarios validados
        if tipo_documento == 'FACTURA':
            DatosFacturacion.objects.create(
                id_comprobante=comprobante,
                rut=str(datos_factura['rut']).strip(),
                razon_social=str(datos_factura['razon_social']).strip(),
                giro=str(datos_factura['giro']).strip(),
                direccion=str(datos_factura['direccion']).strip()
            )
        
        return comprobante