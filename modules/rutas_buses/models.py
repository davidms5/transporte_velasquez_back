from django.db import models

# Create your models here.
class Bus(models.Model):
    """Tabla de autobuses"""
    numero_id = models.CharField(max_length=10, unique=True, db_index=True)
    modelo = models.CharField(max_length=50, db_index=True)
    ruta_asignada = models.ForeignKey('Ruta', null=True, blank=True, on_delete=models.SET_NULL, related_name="buses")

    def __str__(self):
        return f"Bus {self.numero_id} - {self.modelo}"

class Conductor(models.Model):
    """Tabla de conductores"""
    nombre = models.CharField(max_length=100)
    numero_licencia = models.CharField(max_length=20, unique=True, db_index=True)
    dpi = models.CharField(max_length=20, unique=True, db_index=True)
    expiracion_licencia = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.numero_licencia})"

class Horarios(models.Model):
    """Modelo para representar los horarios disponibles de una ruta"""
    time = models.TimeField(unique=True)  # ✅ Horario único

    def __str__(self):
        return self.time.strftime("%H:%M")
    
    
class Ruta(models.Model):
    """Tabla de rutas de buses"""
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # TODO: horario rutas
    bus = models.ManyToManyField(Bus, related_name="rutas")
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    horarios = models.ManyToManyField(Horarios, related_name="routes") 

    def __str__(self):
        return f"Ruta: {self.origen} -> {self.destino}"
