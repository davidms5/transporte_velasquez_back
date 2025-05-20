from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import HorarioPredefinido, Ruta, HorarioRuta
from .serializers.rutas_historial_serializer import RutaSimpleSerializer, AsignacionRutaSerializer, HorarioAsignadoSerializer
from .serializers.horario_ruta_serializer import HorarioPredefinidoSerializer, HorarioRutaCreateSerializer, RutaSerializer, BusSerializer, HorarioRutaSerializer
from .serializers.conductor_bus_serializer import RegistroConductorBusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from rest_framework import generics
from .models import Ruta, Conductor, Bus
from .serializers.conductor_bus_serializer import RutaCreateSerializer, RutaAsignarConductorSerializer, ConductorListaSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import date
from core.permissions import IsAdminOrFacturacion, IsAdminOrSupervisor, IsAdminOrOperador, IsAdminOrFacturacionOrSupervisor
from core.pagination import CustomPaginator

# Create your views here.
class HorarioPredefinidoListView(ListAPIView):
    queryset = HorarioPredefinido.objects.all()
    serializer_class = HorarioPredefinidoSerializer
    
class RegistroConductorBusView(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RegistroConductorBusSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({
                'message': 'Conductor y bus registrados correctamente.',
                'conductor': {
                    'nombre': result['conductor'].nombre,
                    'numero_licencia': result['conductor'].numero_licencia,
                },
                'bus': {
                    'numero_id': result['bus'].numero_id,
                    'modelo': result['bus'].modelo,
                }
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#historial rutas
class HistorialRutasView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        numero_ruta = request.query_params.get('numero_ruta')

        rutas_qs = Ruta.objects.select_related('bus', 'conductor')
        horarios_qs = HorarioRuta.objects.select_related('ruta', 'bus')

        # Aplicamos filtro si se especifica
        if numero_ruta:
            rutas_qs = rutas_qs.filter(numero_ruta=numero_ruta)
            horarios_qs = horarios_qs.filter(ruta__numero_ruta=numero_ruta)

        # Subsets
        rutas_agregadas_qs = rutas_qs.order_by('-id')
        asignaciones_qs = rutas_qs.exclude(conductor__isnull=True).order_by('-id')
        horarios_asignados_qs = horarios_qs.order_by('-id')

        # Paginadores independientes para evitar sobreescritura del estado interno
        paginator_rutas = CustomPaginator()
        paginator_asignaciones = CustomPaginator()
        paginator_horarios = CustomPaginator()

        paginated_rutas = paginator_rutas.paginate_queryset(rutas_agregadas_qs, request)
        paginated_asignaciones = paginator_asignaciones.paginate_queryset(asignaciones_qs, request)
        paginated_horarios = paginator_horarios.paginate_queryset(horarios_asignados_qs, request)

        return Response({
            "rutas_agregadas": RutaSimpleSerializer(paginated_rutas, many=True).data,
            "asignaciones_rutas": AsignacionRutaSerializer(paginated_asignaciones, many=True).data,
            "horarios_asignados": HorarioAsignadoSerializer(paginated_horarios, many=True).data,
            "pagination": {
                "rutas_agregadas": {
                    "page": paginator_rutas.page.number,
                    "total_pages": paginator_rutas.page.paginator.num_pages,
                    "total_items": paginator_rutas.page.paginator.count
                },
                "asignaciones_rutas": {
                    "page": paginator_asignaciones.page.number,
                    "total_pages": paginator_asignaciones.page.paginator.num_pages,
                    "total_items": paginator_asignaciones.page.paginator.count
                },
                "horarios_asignados": {
                    "page": paginator_horarios.page.number,
                    "total_pages": paginator_horarios.page.paginator.num_pages,
                    "total_items": paginator_horarios.page.paginator.count
                }
            }
        })


class CrearRutaView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ruta.objects.all()
    serializer_class = RutaCreateSerializer

class AsignarConductorRutaView(generics.UpdateAPIView):
    
    permission_classes = [IsAuthenticated]
    
    queryset = Ruta.objects.all()
    serializer_class = RutaAsignarConductorSerializer
    lookup_field = 'numero_ruta'


class ListaConductoresView(generics.ListAPIView):
    queryset = Conductor.objects.all().order_by('nombre')
    serializer_class = ConductorListaSerializer

class CrearHorarioRutaView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HorarioRuta.objects.all()
    serializer_class = HorarioRutaCreateSerializer
    
class DatosAsignacionRutaView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Rutas sin conductor
        rutas_sin_conductor = Ruta.objects.filter(conductor__isnull=True)

        # Todos los conductores
        todos_conductores = Conductor.objects.all()

        # Conductores ya asignados
        conductores_asignados_ids = Ruta.objects.exclude(conductor__isnull=True).values_list('conductor__id', flat=True)

        # Conductores no asignados
        conductores_disponibles = todos_conductores.exclude(id__in=conductores_asignados_ids)

        return Response({
            "rutas_sin_conductor": RutaSimpleSerializer(rutas_sin_conductor, many=True).data,
            "conductores_disponibles": [
                {"id": c.id, "nombre": c.nombre} for c in conductores_disponibles
            ]
        }, status=status.HTTP_200_OK)
        

class RutasSinHorarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Rutas sin ningún horario
        rutas_sin_horario = Ruta.objects.filter(horarios__isnull=True).distinct()

        # Todos los buses (puedes aplicar filtros si querés buses "libres")
        buses_disponibles = Bus.objects.all()

        return Response({
            "rutas_sin_horario": RutaSerializer(rutas_sin_horario, many=True).data,
            "buses_disponibles": BusSerializer(buses_disponibles, many=True).data,
        })
        
class RutasConHorarioView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        # Filtra rutas con al menos un horario asignado
        rutas = Ruta.objects.filter(horarios__isnull=False).distinct()
        serializer = RutaSerializer(rutas, many=True)
        return Response(serializer.data)
    
class HorariosDeRutaView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, numero_ruta):
        try:
            ruta = Ruta.objects.get(numero_ruta=numero_ruta) #where bus is not null TODO: y corregir view de admin de ticket para datos que son nulleables
        except Ruta.DoesNotExist:
            return Response({"error": "Ruta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        horarios = ruta.horarios.all()
        serializer = HorarioRutaSerializer(horarios, many=True)
        return Response(serializer.data)