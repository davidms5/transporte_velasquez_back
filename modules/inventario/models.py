from django.db import models

# Create your models here.
class Repuestos(models.Model):
    nombre = models.CharField(max_length=255, unique=True, db_index=True)
    cantidad = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad} disponibles)"
    
class HistorialRepuestos(models.Model):
    """Historial de entradas y salidas de repuestos"""
    repuesto = models.ForeignKey(Repuestos, on_delete=models.CASCADE, related_name="history")
    estado = models.CharField(choices=[('IN', 'Entrada'), ('OUT', 'Salida')], max_length=3)
    cantidad = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repuesto.nombre} - {self.get_estado_display()} - {self.cantidad}"