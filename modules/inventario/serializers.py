from rest_framework import serializers
from .models import Repuestos, HistorialRepuestos

class RepuestosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuestos
        fields = ['nombre', 'descripcion', 'cantidad', 'numero_factura']

class HistorialRepuestosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialRepuestos
        fields = ['repuesto', 'estado', 'cantidad']


# esto puede servir tanto para post como para put de historial TODO: que tambien reciba el id del repuesto
class RepuestoHistorialSerializer(serializers.Serializer):
    """Serializador para manejar el POST que crea un repuesto y su historial"""
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    cantidad = serializers.IntegerField()
    numero_factura = serializers.CharField(required=True)
    estado = serializers.ChoiceField(choices=[('IN', 'Entrada'), ('OUT', 'Salida')])

    def create(self, validated_data):
        """Crea un repuesto y su historial asociado"""
        repuesto, created = Repuestos.objects.get_or_create(
            nombre=validated_data['nombre'],
            defaults={
                'descripcion': validated_data.get('descripcion', ''),
                'cantidad': validated_data['cantidad'],
                'numero_factura': validated_data['numero_factura']
            }
        )

        # Si el repuesto ya existía, actualizamos la cantidad solo si es una entrada
        if not created and validated_data['estado'] == 'IN':
            repuesto.cantidad += validated_data['cantidad']
            repuesto.save()

        historial = HistorialRepuestos.objects.create(
            repuesto=repuesto,
            estado=validated_data['estado'],
            cantidad=validated_data['cantidad']
        )

        return {"repuesto": repuesto, "historial": historial}
