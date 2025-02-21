from django.contrib import admin
from .models import Bus, Conductor, Horarios, Ruta
# Register your models here.

admin.site.register(Bus)
admin.site.register(Conductor)
admin.site.register(Horarios)
admin.site.register(Ruta)