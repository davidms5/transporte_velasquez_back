# modules/ventas/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Factura
from django.conf import settings
from decimal import Decimal

@receiver(post_save, sender=Ticket)
def crear_factura_automatica(sender, instance, created, **kwargs):
    if created:
        iva = Decimal(str(getattr(settings, "IVA")))
        monto_total = round(instance.precio * (Decimal("1.00") + iva), 2)
        
        Factura.objects.create(
            venta=instance,
            monto=monto_total
            )
