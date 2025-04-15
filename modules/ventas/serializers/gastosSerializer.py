from rest_framework import serializers
from ..models import Combustible

class CombustibleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combustible
        fields = ["numero_factura", "proveedor", "cantidad", "uuid_combustible", "created_at"]

        read_only_fields = ["uuid_combustible", "created_at"]
        
class ActualizarCombustibleSerializer(serializers.Serializer):
    numero_factura = serializers.CharField()
    numero_bus = serializers.CharField()
    precio_combustible = serializers.DecimalField(max_digits=10, decimal_places=2)

class CombustibleHistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combustible
        fields = ['numero_factura', 'proveedor', 'cantidad', 'created_at']    