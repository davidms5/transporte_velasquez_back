from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum
from modules.ventas.models import Factura, CierreDiario
from modules.ventas.utils import filtrar_facturas_no_duplicadas

def calcular_cierre_del_dia(facturas_manuales, usuario):
    hoy = timezone.now().date()

    if CierreDiario.objects.filter(fecha=hoy).exists():
        raise ValueError("Ya se registró un cierre para el día de hoy.") # esto no solo evita duplicar, sino sobreescribir cierre ya realizado

    # un validator de facturas manuales duplicadas
    #numeros_manuales = [f["numero_factura"] for f in facturas_manuales]
    #if len(numeros_manuales) != len(set(numeros_manuales)): 
    #    raise ValueError("Hay facturas manuales duplicadas.")
    
    facturas_db = Factura.objects.filter(activo=True, created_at__date=hoy)
    numeros_db = set(facturas_db.values_list("numero_factura", flat=True))

    nuevas_manuales = filtrar_facturas_no_duplicadas(facturas_manuales, numeros_db)

    total_db = facturas_db.aggregate(total=Sum("monto"))["total"] or Decimal("0.00")
    total_manual = sum(Decimal(str(f["monto"])) for f in nuevas_manuales)
    total = total_db + total_manual

    cierre = CierreDiario.objects.create(
        total_facturas=facturas_db.count() + len(nuevas_manuales),
        total_monto=total,
        creado_por=usuario,
    )
    cierre.facturas.set(facturas_db)

    # TODO: para el caso que tqambien haya que registrar las manuales
    #for f in nuevas_manuales:
    #    Factura.objects.create(
    #        numero_factura=f["numero_factura"],
    #        monto=f["monto"],
    #        es_manual=True,  # Podrías tener este campo booleano en el modelo
    #        activo=True,
    #    )
    #cierre.facturas.add(*facturas_manual_creadas)
    return cierre, nuevas_manuales
