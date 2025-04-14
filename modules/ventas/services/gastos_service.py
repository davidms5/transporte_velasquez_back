from ..models import Combustible

def registrar_combustible(validated_data):
    return Combustible.objects.create(**validated_data)