# serializers.py

from rest_framework import serializers
from ..models import Factura

class FacturaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['codigo', 'proveedor', 'numero_factura', 'cai']


class FacturaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['proveedor', 'cai']  # no permitimos editar 'codigo' ni 'numero_factura'


class FacturaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['id', 'codigo', 'proveedor', 'numero_factura', 'cai']
