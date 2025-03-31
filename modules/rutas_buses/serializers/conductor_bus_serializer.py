# serializers.py

from rest_framework import serializers
from ..models import Conductor, Bus, Ruta

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = ['nombre', 'numero_licencia', 'dpi', 'expiracion_licencia']


class BusSerializer(serializers.ModelSerializer):
    ruta_asignada = serializers.SlugRelatedField(
        slug_field='numero_ruta',
        queryset=Ruta.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Bus
        fields = ['numero_id', 'modelo', 'ruta_asignada']


class RegistroConductorBusSerializer(serializers.Serializer):
    conductor = ConductorSerializer()
    bus = BusSerializer()

    def create(self, validated_data):
        from django.db import transaction

        conductor_data = validated_data['conductor']
        bus_data = validated_data['bus']

        with transaction.atomic():
            conductor = Conductor.objects.create(**conductor_data)
            bus = Bus.objects.create(**bus_data) #TODO:: agregar la opcion de que no se pueda agregar la ruta aqui, ya que aun no puede estar asignada

        return {
            'conductor': conductor,
            'bus': bus
        }


class RutaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['numero_ruta', 'origen', 'destino', 'precio']


class RutaAsignarConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['conductor']
    
    def validate_conductor(self, conductor):
        ruta_actual = self.instance

        # Buscar si el conductor ya está asignado a otra ruta distinta
        ruta_existente = Ruta.objects.filter(conductor=conductor).exclude(id=ruta_actual.id).first()
        if ruta_existente:
            raise serializers.ValidationError(
                f"El conductor ya está asignado a la ruta {ruta_existente.numero_ruta}."
            )

        return conductor


class ConductorListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = ['id', 'nombre']
