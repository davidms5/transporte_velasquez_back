# serializers.py

from rest_framework import serializers
from ..models import Ruta, HorarioRuta

class RutaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['numero_ruta', 'origen', 'destino', 'precio']


class AsignacionRutaSerializer(serializers.ModelSerializer):
    conductor = serializers.StringRelatedField()

    class Meta:
        model = Ruta
        fields = ['numero_ruta', 'conductor']


class HorarioAsignadoSerializer(serializers.ModelSerializer):
    ruta = serializers.StringRelatedField()
    bus = serializers.StringRelatedField()

    class Meta:
        model = HorarioRuta
        fields = ['ruta', 'bus', 'dia', 'hora_salida', 'hora_llegada']
