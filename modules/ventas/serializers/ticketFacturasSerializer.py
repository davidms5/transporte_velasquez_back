from rest_framework import serializers
from ..models import Ticket, Factura
from modules.rutas_buses.models import HorarioRuta
from decimal import Decimal
from django.conf import settings

class TicketCreateSerializer(serializers.ModelSerializer):
    numero_factura = serializers.SerializerMethodField()
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
            'created_at',
            'numero_factura',  # Campo adicional en la respuesta
            "precio_con_iva"
        ]

    read_only_fields = ['created_at', 'numero_factura', "precio_con_iva"]
    
    def validate(self, data):
        cliente_dpi = data.get("cliente_dpi")
        responsable_dpi = data.get("responsable_dpi")

        if responsable_dpi and cliente_dpi == responsable_dpi:
            raise serializers.ValidationError({
                "responsable_dpi": "El DPI del responsable no puede ser igual al del cliente."
            })

        return data

    def get_numero_factura(self, obj):
        factura = Factura.objects.filter(venta=obj).first()
        return factura.numero_factura if factura else None
    
    def create(self, validated_data):
        iva = Decimal(str(getattr(settings, "IVA")))
        precio = validated_data["precio"]
        total = round(precio * (Decimal("1.00") + iva), 2)
        
        validated_data["precio_con_iva"] = total
        ticket = Ticket.objects.create(**validated_data)

        # Crear la factura automáticamente
        #Factura.objects.create(venta=ticket)

        return ticket
    
    
    
class FacturaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='venta.cliente_nombre', read_only=True)

    class Meta:
        model = Factura
        fields = ['id', 'numero_factura', 'cliente_nombre', 'created_at']
        
class VentaReporteSerializer(serializers.ModelSerializer):
    numero_ruta = serializers.CharField(source="venta.horario_ruta.ruta.numero_ruta")
    hora_salida = serializers.TimeField(source="venta.horario_ruta.hora_salida")
    hora_llegada = serializers.TimeField(source="venta.horario_ruta.hora_llegada")

    class Meta:
        model = Factura
        fields = ["numero_factura", "numero_ruta", "hora_salida", "hora_llegada"]