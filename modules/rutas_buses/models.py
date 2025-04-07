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

class Ruta(models.Model):
    """Tabla de rutas de buses"""
    numero_ruta = models.CharField(max_length=10, unique=True, db_index=True)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # TODO: horario rutas
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="rutas")
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ruta: {self.origen} -> {self.destino}"

class HorarioRuta(models.Model):
    DIAS_SEMANA = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]

    ruta = models.ForeignKey("Ruta", on_delete=models.CASCADE, related_name="horarios")
    bus = models.ForeignKey("Bus", on_delete=models.CASCADE, related_name="horarios")
    #conductor = models.ForeignKey("Conductor", on_delete=models.SET_NULL, null=True, blank=True, related_name="horarios")
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_salida = models.TimeField()
    hora_llegada = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('ruta', 'bus', 'dia', 'hora_salida')

    def __str__(self):
        return f"{self.ruta.numero_ruta} - {self.bus.numero_id} - {self.get_dia_display()} {self.hora_salida.strftime('%H:%M')}"
    
    
# models.py

class HorarioPredefinido(models.Model):
    hora_salida = models.TimeField(unique=True)

    def __str__(self):
        return self.hora_salida.strftime('%H:%M')

    class Meta:
        ordering = ['hora_salida']
        verbose_name = 'Horario Predefinido'
        verbose_name_plural = 'Horarios Predefinidos'
