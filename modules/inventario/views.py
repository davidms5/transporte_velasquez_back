from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Repuestos, HistorialRepuestos, Factura
from .serializers.serializers import RepuestoHistorialSerializer, HistorialRepuestosSerializer, RepuestosSerializer
from .serializers.factura_serializers import FacturaCreateSerializer, FacturaDetailSerializer, FacturaUpdateSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from core.permissions import IsAdminOrFacturacion, IsAdminOrSupervisor

#Post repuesto mas historial
@method_decorator(csrf_exempt, name='dispatch')
class RegistrarRepuestoAPIView(APIView):
    """Endpoint para registrar un repuesto y su historial"""
    permission_classes = [IsAuthenticated]  # TODO: que sea supervisor y/o operador

    def post(self, request):
        repuesto_id = request.data.get('repuesto_id')
        serializer = RepuestoHistorialSerializer(data=request.data)
        
        #if serializer.is_valid():
        #    historial = serializer.save()
        #    respuesta = HistorialRepuestosSerializer(historial)
        #    return Response(respuesta.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            if repuesto_id:
                try:
                    repuesto = Repuestos.objects.get(id=repuesto_id)
                    historial = serializer.update(repuesto, serializer.validated_data)
                except Repuestos.DoesNotExist:
                    return Response({"error": "Repuesto no encontrado."}, status=404)
            else:
                historial = serializer.create(serializer.validated_data)

            return Response({"mensaje": "Operación exitosa", "id_historial": historial.id}, status=201)

        return Response(serializer.errors, status=400)
    
class RepuestosListView(ListAPIView):
      
    queryset = Repuestos.objects.filter(cantidad__gt=0).order_by('id')
    serializer_class = RepuestosSerializer
    pagination_class = None

class HistorialRepuestosListView(ListAPIView):
    permission_classes = [IsAuthenticated]
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
    
#Factura views TODO: luego separar en una carpeta aparte de views

class FacturaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Factura.objects.filter(activo=True).order_by('-id')
    serializer_class = FacturaDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FacturaCreateSerializer
        return FacturaDetailSerializer


class FacturaRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    
    queryset = Factura.objects.filter(activo=True)
    lookup_field = 'codigo'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return FacturaUpdateSerializer
        return FacturaDetailSerializer


class FacturaSoftDeleteView(generics.DestroyAPIView):
    queryset = Factura.objects.filter(activo=True)
    serializer_class = FacturaDetailSerializer
    lookup_field = 'codigo'

    def delete(self, request, *args, **kwargs):
        factura = self.get_object()
        factura.activo = False
        factura.save()
        return Response({"detail": "Factura eliminada."}, status=status.HTTP_204_NO_CONTENT) #soft delete