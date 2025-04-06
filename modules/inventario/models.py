from django.db import models

# Create your models here.

class Factura(models.Model):
    codigo = models.CharField(max_length=50, db_index=True)  # Código de factura
    proveedor = models.CharField(max_length=255)
    numero_factura = models.CharField(max_length=100)
    cai = models.CharField(max_length=100)  # Código de autorización de impresión
    activo = models.BooleanField(default=True)  # Soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Factura {self.codigo} - {self.proveedor}"
    
    
class Repuestos(models.Model):
    nombre = models.CharField(max_length=255, db_index=True)
    cantidad = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)  # Campo opcional de texto
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="repuestos")
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad} disponibles)"
    
class HistorialRepuestos(models.Model):
    """Historial de entradas y salidas de repuestos"""
    repuesto = models.ForeignKey(Repuestos, on_delete=models.CASCADE, related_name="history")
    estado = models.CharField(choices=[('IN', 'Entrada'), ('OUT', 'Salida')], max_length=3)
    cantidad = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'inventario_historial_repuestos'  # <- Nombre personalizado de la tabla TODO: descomentar y arreglar relacion en base de datos

    def __str__(self):
        return f"{self.repuesto.nombre} - {self.get_estado_display()} - {self.cantidad}"
    
    

