from django.contrib import admin
from .models import Factura, Repuestos, HistorialRepuestos


# Register your models here. TODO:; ajustar nombres de modelos
admin.site.register(Repuestos)
#admin.site.register(HistorialRepuestos)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
