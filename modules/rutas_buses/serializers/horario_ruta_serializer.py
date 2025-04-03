# serializers.py

from rest_framework import serializers
from ..models import HorarioRuta, Ruta, Bus, HorarioPredefinido
from datetime import timedelta

class HorarioRutaCreateSerializer(serializers.ModelSerializer):
    ruta = serializers.SlugRelatedField(slug_field='numero_ruta', queryset=Ruta.objects.all())
    bus = serializers.SlugRelatedField(slug_field='numero_id', queryset=Bus.objects.all())

    class Meta:
        model = HorarioRuta
        fields = ['ruta', 'bus', 'dia', 'hora_salida', 'hora_llegada']

    def validate(self, data):
        ruta = data['ruta']
        bus = data['bus']
        dia = data['dia']
        hora_salida = data['hora_salida']
        hora_llegada = data['hora_llegada']

        # Validación de conflicto: verificar si el bus ya está asignado en ese rango horario
        conflicto = HorarioRuta.objects.filter(
            bus=bus,
            dia=dia,
            hora_salida__lt=hora_llegada,
            hora_llegada__gt=hora_salida
        ).exclude(ruta=ruta)  # opcional: permitir solapamiento en la misma ruta

        if conflicto.exists():
            raise serializers.ValidationError(
                f"El bus ya está asignado a otra ruta en ese rango horario ({dia} {hora_salida}-{hora_llegada})."
            )

        return data
    
class HorarioPredefinidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioPredefinido
        fields = ['hora_salida']

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['numero_ruta', 'origen', 'destino']

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['numero_id', 'modelo']
