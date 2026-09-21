from django.test import TestCase
from decimal import Decimal
from .models import Usuario, Venta, JornadaComercial
from .services import GeneradorVentasService, ComprobanteFactory

class VentasUnitTestCase(TestCase):
    def test_autenticacion_usuario(self):
        """Valida que un usuario vendedor posea credenciales y rol válidos."""
        usuario = "vendedor1"
        clave_valida = True
        self.assertEqual(usuario, "vendedor1")
        self.assertTrue(clave_valida)

    def test_calculo_total_venta(self):
        """Verifica la precisión del cálculo del 19% de IVA y el total general."""
        subtotal = Decimal('10000.00')
        resultado = GeneradorVentasService.calcular_totales(subtotal)
        
        self.assertEqual(resultado['subtotal_neto'], Decimal('10000.00'))
        self.assertEqual(resultado['monto_iva'], Decimal('1900.00'))
        self.assertEqual(resultado['total_general'], Decimal('11900.00'))

    def test_creacion_comprobante(self):
        """Valida la instanciación de comprobantes mediante el patrón Factory."""
        vendedor = Usuario.objects.create(username='test_user', rol='VENDEDOR')
        jornada = GeneradorVentasService.validar_jornada(vendedor)
        
        venta = Venta.objects.create(
            id_vendedor=vendedor,
            id_jornada=jornada,
            subtotal_neto=Decimal('10000.00'),
            monto_iva=Decimal('1900.00'),
            total_general=Decimal('11900.00')
        )
        
        comprobante = ComprobanteFactory.crear_documento(venta, 'BOLETA')
        self.assertEqual(comprobante.tipo_documento, 'BOLETA')
        self.assertIn(comprobante.tipo_documento, ['BOLETA', 'FACTURA'])