from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#from .models import Repuestos, HistorialRepuestos
from .serializers import RepuestoHistorialSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegistrarRepuestoAPIView(APIView):
    """Endpoint para registrar un repuesto y su historial"""
    permission_classes = [IsAuthenticated]  # Requiere autenticación JWT

    def post(self, request):
        serializer = RepuestoHistorialSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                "message": "Repuesto registrado exitosamente",
                "repuesto": {
                    "nombre": data["repuesto"].nombre,
                    "descripcion": data["repuesto"].descripcion,
                    "cantidad": data["repuesto"].cantidad,
                    "numero_factura": data["repuesto"].numero_factura
                },
                "historial": {
                    "estado": data["historial"].get_estado_display(),
                    "cantidad": data["historial"].cantidad,
                    "timestamp": data["historial"].timestamp
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

