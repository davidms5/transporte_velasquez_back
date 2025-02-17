from django.db import models
from modules.rutas_buses.models import Ruta
# Create your models here.

class Ticket(models.Model):
    """Registro de venta de boletos"""
    cliente_nombre = models.CharField(max_length=255)
    cliente_dpi = models.CharField(max_length=20)
    es_adulto = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boleto {self.pk} - {self.cliente_nombre}"

class Factura(models.Model):
    """Tabla de facturas generadas"""
    venta = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20, unique=True)
    logo = models.ImageField(upload_to="facturas/", null=True) #TODO: ver como hacer un serializer para subir el logo por la api

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.venta.cliente_nombre}"
