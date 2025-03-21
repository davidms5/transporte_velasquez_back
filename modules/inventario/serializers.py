from rest_framework import serializers
from .models import Repuestos, HistorialRepuestos
from django.db.models import Q

class RepuestosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuestos
        fields = ['nombre', 'descripcion', 'cantidad', 'numero_factura']


class HistorialRepuestosSerializer(serializers.ModelSerializer):
    repuesto = RepuestosSerializer()
    timestamp = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    descripcion_detalle = serializers.SerializerMethodField()
    class Meta:
        model = HistorialRepuestos
        fields = ['repuesto', 'estado', 'cantidad', "timestamp", "descripcion_detalle"]
        
    def get_descripcion_detalle(self, obj):
        return str(obj)


# esto puede servir tanto para post como para put de historial TODO: revisar que estado = 'IN' no tenga redundancias en el serializer
class RepuestoHistorialSerializer(serializers.Serializer):
    """Serializador para manejar el POST que crea un repuesto y su historial"""
    repuesto_id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    cantidad = serializers.IntegerField(min_value=1)
    numero_factura = serializers.CharField(required=True)
    estado = serializers.ChoiceField(choices=[('IN', 'Entrada'), ('OUT', 'Salida')], required=False, default='IN')

    def create(self, validated_data):
        """Crea un repuesto y su historial asociado"""
        repuesto = None
        repuesto_id = validated_data.get("repuesto_id")
        estado = validated_data.get('estado', 'IN')
        
        if repuesto_id:
            try:
                repuesto = Repuestos.objects.get(id=repuesto_id)
            except Repuestos.DoesNotExist:
                raise serializers.ValidationError("Repuesto no encontrado con ese ID")
        
        if not repuesto:
            # Si no se encuentra el repuesto, lo creamos y forzamos estado 'IN'
            
            nombre = validated_data['nombre']
            numero_factura = validated_data['numero_factura']

            if Repuestos.objects.filter(Q(nombre=nombre) | Q(numero_factura=numero_factura)).exists():
                raise serializers.ValidationError(
                    "Ya existe un repuesto con ese nombre o número de factura."
                )
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
            elif estado == 'OUT':
                if repuesto.cantidad < validated_data['cantidad']:
                    raise serializers.ValidationError("No hay suficiente stock para realizar la salida.")
                repuesto.cantidad -= validated_data['cantidad']
                repuesto.save()
            

        historial = HistorialRepuestos.objects.create(
            repuesto=repuesto,
            estado=estado,
            cantidad=validated_data['cantidad']
        )

        return historial
