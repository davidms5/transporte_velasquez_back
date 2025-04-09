from django.test import TestCase

# Create your tests here.
import pytest
from decimal import Decimal
from django.utils import timezone
from modules.ventas.models import Factura, Ticket, CierreDiario
from modules.ventas.services import calcular_cierre_del_dia

@pytest.mark.django_db
def test_calcular_cierre_del_dia_con_facturas_manuales():
    # Crear ticket y factura en base
    ticket = Ticket.objects.create(
        cliente_nombre="Juan",
        cliente_dpi="0801199912345",
        es_adulto=True,
        precio=Decimal("100.00"),
        horario_ruta_id=1,  # depende de tus fixtures
    )
    factura = Factura.objects.create(venta=ticket, numero_factura="F-BASE-0001", activo=True)

    # Factura manual no repetida
    manuales = [
        {"numero_factura": "F-MAN-0002", "numero_ruta": "RUTA-01", "monto": "150.00"},
        {"numero_factura": "F-MAN-0003", "numero_ruta": "RUTA-02", "monto": "200.00"}
    ]

    cierre, nuevas_manuales = calcular_cierre_del_dia(manuales)

    assert cierre.total_facturas == 3
    assert cierre.total_monto == Decimal("450.00")
    assert cierre.facturas.count() == 1  # solo 1 desde base
    assert len(nuevas_manuales) == 2
