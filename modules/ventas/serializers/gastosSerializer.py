from rest_framework import serializers
from ..models import Combustible, GastoCompra

class CombustibleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combustible
        fields = ["numero_factura", "precio_combustible", "cantidad", "uuid_combustible", "created_at"]

        read_only_fields = ["uuid_combustible", "created_at"]
        
class ActualizarCombustibleSerializer(serializers.Serializer):
    numero_factura = serializers.CharField()
    numero_bus = serializers.CharField()
    precio_combustible = serializers.DecimalField(max_digits=10, decimal_places=2)

class CombustibleHistorialSerializer(serializers.ModelSerializer):
    bus_numero_id = serializers.CharField(source="bus.numero_id", default=None)
    class Meta:
        model = Combustible
        fields = ['numero_factura', 'proveedor', 'cantidad','precio_combustible', "bus_numero_id", 'created_at']    
        
class GastoCompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastoCompra
        fields = ["numero_factura", "proveedor", "cantidad"]
