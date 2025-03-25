from django.contrib import admin
from .models import HorarioPredefinido, Bus, Ruta, HorarioRuta
# Register your models here.
admin.site.register(HorarioPredefinido)
admin.site.register(Bus)
admin.site.register(Ruta)
admin.site.register(HorarioRuta)