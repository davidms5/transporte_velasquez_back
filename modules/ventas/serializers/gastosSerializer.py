from rest_framework import serializers
from ..models import Combustible

class CombustibleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combustible
        fields = ["numero_factura", "proveedor", "cantidad", "uuid_combustible", "created_at"]

        read_only_fields = ["uuid_combustible", "created_at"]