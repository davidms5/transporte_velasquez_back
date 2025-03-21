from django.db import models

# Create your models here.
class Repuestos(models.Model):
    nombre = models.CharField(max_length=255, unique=True, db_index=True)
    cantidad = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)  # Campo opcional de texto
    numero_factura = models.CharField(max_length=50, blank=True, unique=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad} disponibles)"
    
class HistorialRepuestos(models.Model):
    """Historial de entradas y salidas de repuestos"""
    repuesto = models.ForeignKey(Repuestos, on_delete=models.CASCADE, related_name="history")
    estado = models.CharField(choices=[('IN', 'Entrada'), ('OUT', 'Salida')], max_length=3)
    cantidad = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    #class Meta:
    #    db_table = 'inventario_historial_repuestos'  # <- Nombre personalizado de la tabla TODO: descomentar y arreglar relacion en base de datos

    def __str__(self):
        return f"{self.repuesto.nombre} - {self.get_estado_display()} - {self.cantidad}"