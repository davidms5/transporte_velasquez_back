from rest_framework import serializers
from ..models import Ticket, Factura
from modules.rutas_buses.models import HorarioRuta


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "cliente_nombre",
            "cliente_dpi",
            "es_adulto",
            "precio",
            "partida_nacimiento_id",
            "responsable_menor",
            "responsable_dpi",
            "horario_ruta",
        ]

    def create(self, validated_data):
        ticket = Ticket.objects.create(**validated_data)

        # Crear la factura automáticamente
        #Factura.objects.create(venta=ticket)

        return ticket