from rest_framework import serializers
from .models import Repuestos

def validar_repuesto_unico(nombre, numero_factura):
    """
    Verifica si ya existe un repuesto con el mismo nombre o número de factura.
    Lanza ValidationError si encuentra coincidencias.
    """
    if Repuestos.objects.filter(nombre=nombre).exists():
        raise serializers.ValidationError("Ya existe un repuesto con ese nombre.")
    
    if Repuestos.objects.filter(numero_factura=numero_factura).exists():
        raise serializers.ValidationError("Ya existe un repuesto con ese número de factura.")
