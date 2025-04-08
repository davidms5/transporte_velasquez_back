# modules/ventas/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Factura

@receiver(post_save, sender=Ticket)
def crear_factura_automatica(sender, instance, created, **kwargs):
    if created:
        Factura.objects.create(venta=instance)
