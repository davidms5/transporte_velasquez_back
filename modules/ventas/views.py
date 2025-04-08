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