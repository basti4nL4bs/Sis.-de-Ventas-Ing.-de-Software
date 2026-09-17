from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from decimal import Decimal
from .models import Producto, Venta, DetalleVenta, Usuario
from .serializers import ProductoSerializer, ComprobanteSerializer
from .services import GeneradorVentasService, ComprobanteFactory

@api_view(['GET'])
@permission_classes([AllowAny])
def listar_productos(request):
    """Retorna el catálogo de productos al frontend."""
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic # Garantiza las propiedades ACID: si algo falla, no se guarda nada a medias
def registrar_venta(request):
    """Procesa el carrito de compras, aplica impuestos y genera el comprobante."""
    try:
        items = request.data.get('items', [])
        tipo_documento = request.data.get('tipo_documento', 'BOLETA')
        datos_factura = request.data.get('datos_factura', None)
        
        if not items:
            return Response({'error': 'La venta debe contener al menos un producto.'}, status=status.HTTP_400_BAD_REQUEST)

        # Para el prototipo, asignamos al primer usuario disponible o creamos un Admin
        vendedor = Usuario.objects.first()
        if not vendedor:
            vendedor = Usuario.objects.create(username='admin', rol='JEFE_VENTAS')
        
        # 1. Validar estado de la jornada comercial
        jornada = GeneradorVentasService.validar_jornada(vendedor)
        if jornada.estado == 'CERRADO':
            return Response({'error': 'Jornada comercial cerrada. No se pueden registrar ventas'}, status=status.HTTP_403_FORBIDDEN)

        # 2. Calcular el Subtotal Neto
        subtotal_neto = Decimal('0.00')
        for item in items:
            producto = Producto.objects.get(codigo=item['codigo'])
            subtotal_neto += producto.precio_unitario * int(item['cantidad'])

        # 3. Aplicar 19% de IVA y calcular el Total General
        totales = GeneradorVentasService.calcular_totales(subtotal_neto)

        # 4. Registrar la Venta
        venta = Venta.objects.create(
            id_vendedor=vendedor,
            id_jornada=jornada,
            subtotal_neto=totales['subtotal_neto'],
            monto_iva=totales['monto_iva'],
            total_general=totales['total_general']
        )

        # 5. Registrar el Detalle de los productos vendidos
        for item in items:
            producto = Producto.objects.get(codigo=item['codigo'])
            DetalleVenta.objects.create(
                id_venta=venta,
                codigo_producto=producto,
                cantidad=int(item['cantidad']),
                precio_unitario=producto.precio_unitario
            )

        # 6. Patrón Factory: Generar Boleta o Factura dinámicamente
        comprobante = ComprobanteFactory.crear_documento(venta, tipo_documento, datos_factura)

        return Response({
            'mensaje': 'Venta registrada con éxito',
            'comprobante': ComprobanteSerializer(comprobante).data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)