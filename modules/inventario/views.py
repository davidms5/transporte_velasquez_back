from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Repuestos, HistorialRepuestos
from .serializers import RepuestoHistorialSerializer, HistorialRepuestosSerializer, RepuestosSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#Post repuesto mas historial
@method_decorator(csrf_exempt, name='dispatch')
class RegistrarRepuestoAPIView(APIView):
    """Endpoint para registrar un repuesto y su historial"""
    permission_classes = [IsAuthenticated]  # Requiere autenticación JWT

    def post(self, request):
        serializer = RepuestoHistorialSerializer(data=request.data)
        
        if serializer.is_valid():
            historial = serializer.save()
            respuesta = HistorialRepuestosSerializer(historial)
            return Response(respuesta.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RepuestosListView(ListAPIView):
    queryset = Repuestos.objects.all().order_by('id')
    serializer_class = RepuestosSerializer

class HistorialRepuestosListView(ListAPIView):
    queryset = HistorialRepuestos.objects.select_related('repuesto').order_by('-timestamp')
    serializer_class = HistorialRepuestosSerializer

class RepuestoDetailCustomView(APIView):
    def get(self, request, id):
        try:
            repuesto = Repuestos.objects.get(id=id)
        except Repuestos.DoesNotExist:
            return Response({"error": "Repuesto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RepuestosSerializer(repuesto)
        return Response(serializer.data)