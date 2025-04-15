from ..models import Combustible, Bus
from django.core.exceptions import ObjectDoesNotExist

class CombustibleService:
    @staticmethod
    def actualizar_precio_combustible(numero_factura: str, numero_bus: str, nuevo_precio):
        try:
            bus = Bus.objects.get(numero_id=numero_bus)
        except Bus.DoesNotExist:
            raise ObjectDoesNotExist("Bus no encontrado.")

        try:
            combustible = Combustible.objects.get(numero_factura=numero_factura, bus=bus)
        except Combustible.DoesNotExist:
            raise ObjectDoesNotExist("Registro de combustible no encontrado para esa factura o bus.")

        combustible.precio_combustible = nuevo_precio
        combustible.save()

        return combustible
