from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Ticket, Factura, Combustible, CierreDiario, GastoCompra
from .serializers.ticketFacturasSerializer import TicketCreateSerializer, FacturaSerializer, VentaReporteSerializer, CierreDiarioResponseSerializer
from .serializers.gastosSerializer import CombustibleCreateSerializer, ActualizarCombustibleSerializer, CombustibleHistorialSerializer, GastoCompraCreateSerializer, GastoCompraHistorialSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from modules.ventas.services.cierre_diario_service import calcular_cierre_del_dia
from .services.gastos_service import registrar_combustible
from .services.combustible_service import CombustibleService
from core.permissions import IsAdminOrSupervisor
from django.db.models import Count, F, DecimalField, ExpressionWrapper
from core.permissions import IsAdminOrFacturacion
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
# Create your views here.
class CrearTicketView(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    
    serializer_class = TicketCreateSerializer
    
    
class FacturasActivasView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    
    serializer_class = FacturaSerializer
    

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
    
    permission_classes = [IsAuthenticated]
    
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
        
class ResumenPorRutaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fecha_str = request.query_params.get("fecha")
        fecha = fecha_str or now().date()

        tickets = Ticket.objects.filter(created_at__date=fecha)

        resumen = (
            tickets
            .values("horario_ruta__ruta__numero_ruta", "horario_ruta__ruta__precio")
            .annotate(
                boletos_vendidos=Count("id"),
                monto_total=ExpressionWrapper(
                    F("horario_ruta__ruta__precio") * Count("id"),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )
        )

        # Formatear la respuesta
        resultado = []
        for item in resumen:
            resultado.append({
                "numero_ruta": item["horario_ruta__ruta__numero_ruta"],
                "boletos_vendidos": item["boletos_vendidos"],
                "precio_unitario": float(item["horario_ruta__ruta__precio"]),
                "monto_total": float(item["monto_total"]),
                "fecha": str(fecha)
            })

        return Response(resultado)
    
class RegistroFacturaCombustibleView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Combustible.objects.all()
    serializer_class = CombustibleCreateSerializer
    
    def perform_create(self, serializer):
        #registrar_combustible(serializer.validated_data)
        serializer.save()
        
class ActualizarCombustibleView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ActualizarCombustibleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            combustible = CombustibleService.actualizar_precio_combustible(
                numero_factura=serializer.validated_data['numero_factura'],
                numero_bus=serializer.validated_data['numero_bus'],
                nuevo_precio=serializer.validated_data['precio_combustible']
            )
            return Response({
                "mensaje": "Monto de gasolina actualizado correctamente.",
                "uuid_combustible": str(combustible.uuid_combustible),
                "updated_at": combustible.updated_at
            }, status=200)

        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=404)

        except Exception as e:
            return Response({"error": "Error inesperado."}, status=500)
        
class HistorialCombustibleView(APIView):
    def get(self, request):
        fecha_str = request.query_params.get('fecha')  # formato: YYYY-MM-DD

        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)
        else:
            fecha = timezone.localdate()

        queryset_combustible = Combustible.objects.filter(created_at__date=fecha).order_by('-created_at')
        serializer_combustible = CombustibleHistorialSerializer(queryset_combustible, many=True)
        
        queryset = GastoCompra.objects.filter(created_at__date=fecha).order_by('-created_at')
        serializer_gastos_compras = GastoCompraHistorialSerializer(queryset, many=True)
        
        data_total = serializer_gastos_compras.data #serializer_combustible.data +
        return Response(data_total, status=200)
    
class CierreDiarioDetailView(APIView):
    def get(self, request):
        fecha_str = request.query_params.get("fecha")

        # Fecha actual por defecto
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else timezone.localdate()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)

        try:
            cierre = CierreDiario.objects.get(creado_en__date=fecha)
        except CierreDiario.DoesNotExist:
            return Response({"error": "No se encontró un cierre para esta fecha."}, status=404)
        
        data = {
            "fecha": fecha,
            "total_facturas": cierre.total_facturas,
            "total_monto": cierre.total_monto
        }

        serializer = CierreDiarioResponseSerializer(data)
        return Response(serializer.data, status=200)
    
class GastoCompraCreateView(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    
    queryset = GastoCompra.objects.all()
    serializer_class = GastoCompraCreateSerializer
    