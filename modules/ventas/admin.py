from django.contrib import admin
from .models import Ticket, Factura
# Register your models here.
#admin.site.register(Ticket)
@admin.register(Ticket)
class FacturaAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False