from django.db import models
from modules.rutas_buses.models import HorarioRuta
import uuid
from django.utils import timezone
# Create your models here.

class Ticket(models.Model):
    """Registro de venta de boletos"""
    cliente_nombre = models.CharField(max_length=255)
    cliente_dpi = models.CharField(max_length=20, db_index=True)
    es_adulto = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    #ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    #responsable en el caso de que el ticket sea de un menor
    partida_nacimiento_id = models.CharField(null=True, max_length=20)
    responsable_menor = models.CharField(null=True, max_length=255)
    responsable_dpi = models.CharField(null=True, max_length=20, db_index=True)
    
    horario_ruta = models.ForeignKey(HorarioRuta, on_delete=models.CASCADE, related_name="tickets")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boleto {self.pk} - {self.cliente_nombre}"

class Factura(models.Model):
    """Tabla de facturas generadas"""
    venta = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20, unique=True, db_index=True)
    #logo = models.ImageField(upload_to="facturas/", null=True) #TODO: ver como hacer un serializer para subir el logo por la api
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.venta.cliente_nombre}"

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            fecha = timezone.now().strftime("%Y%m%d")
            correlativo = str(uuid.uuid4().int)[:6]  # parte aleatoria única
            self.numero_factura = f"F-{fecha}-{correlativo}"
        super().save(*args, **kwargs)
