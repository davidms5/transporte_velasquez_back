from rest_framework import serializers
from .models import Repuestos, HistorialRepuestos

class RepuestosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuestos
        fields = ['nombre', 'descripcion', 'cantidad', 'numero_factura']

class HistorialRepuestosSerializer(serializers.ModelSerializer):
    repuesto = RepuestosSerializer()
    class Meta:
        model = HistorialRepuestos
        fields = ['repuesto', 'estado', 'cantidad']


# esto puede servir tanto para post como para put de historial TODO: que tambien reciba el id del repuesto
class RepuestoHistorialSerializer(serializers.Serializer):
    """Serializador para manejar el POST que crea un repuesto y su historial"""
    repuesto_id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    cantidad = serializers.IntegerField()
    numero_factura = serializers.CharField(required=True)
    estado = serializers.ChoiceField(choices=[('IN', 'Entrada'), ('OUT', 'Salida')])

    def create(self, validated_data):
        """Crea un repuesto y su historial asociado"""
        repuesto = None
        repuesto_id = validated_data.get("repuesto_id")
        estado = validated_data['estado']
        
        if repuesto_id:
            try:
                repuesto = Repuestos.objects.get(id=repuesto_id)
            except Repuestos.DoesNotExist:
                raise serializers.ValidationError("Repuesto no encontrado con ese ID")
        
        if not repuesto:
            # Si no se encuentra el repuesto, lo creamos y forzamos estado 'IN'
            repuesto = Repuestos.objects.create(
                nombre=validated_data['nombre'],
                descripcion=validated_data.get('descripcion', ''),
                cantidad=validated_data['cantidad'],
                numero_factura=validated_data['numero_factura']
            )
            estado = 'IN'  # Forzamos estado IN al crearlo
        else:
            # Si ya existe y es una entrada, actualizamos la cantidad
            if estado == 'IN':
                repuesto.cantidad += validated_data['cantidad']
                repuesto.save()
            

        historial = HistorialRepuestos.objects.create(
            repuesto=repuesto,
            estado=validated_data['estado'],
            cantidad=validated_data['cantidad']
        )

        return historial
