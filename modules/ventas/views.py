from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Ticket, Factura
from .serializers.ticketFacturasSerializer import TicketCreateSerializer, FacturaSerializer, VentaReporteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from modules.ventas.services.cierre_diario_service import calcular_cierre_del_dia
from core.permissions import IsAdminOrSupervisor
# Create your views here.
class CrearTicketView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]
    
class FacturasActivasView(generics.ListAPIView):
    serializer_class = FacturaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Factura.objects.filter(activo=True).order_by('-created_at')
    
class AnularFacturaView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, numero_factura):
        try:
            factura = Factura.objects.get(numero_factura=numero_factura, activo=True)
            factura.activo = False
            factura.save()  # ✅ updated_at se actualiza automáticamente
            return Response({"detail": "Factura anulada correctamente."}, status=status.HTTP_200_OK)
        except Factura.DoesNotExist:
            return Response({"detail": "Factura no encontrada o ya anulada."}, status=status.HTTP_404_NOT_FOUND)
        
class ReporteVentasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fecha_str = request.query_params.get("fecha")
        fecha = parse_date(fecha_str) if fecha_str else now().date()

        facturas = Factura.objects.filter(
            #created_at__date=fecha, TODO: agregarfiltro por fecha
            activo=True  # solo facturas activas
        ).select_related("venta__horario_ruta__ruta")

        serializer = VentaReporteSerializer(facturas, many=True)
        return Response(serializer.data)
    
class CierreDiarioView(APIView):
    
    permission_classes = [IsAdminOrSupervisor]
    
    def post(self, request):
        try:
            facturas_manuales = request.data.get("facturas_manuales", [])
            cierre, nuevas_manuales = calcular_cierre_del_dia(facturas_manuales, request.user) #esto ignora las facturas manuales duplicadas de las guardadas en la base de datos

            return Response({
                "mensaje": "Cierre del día generado correctamente.",
                "fecha": str(cierre.fecha),
                "total_facturas": cierre.total_facturas,
                "total_monto": str(cierre.total_monto),
                "manuales_registradas": nuevas_manuales
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Error inesperado al procesar el cierre."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)