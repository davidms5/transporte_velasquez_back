from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import HorarioPredefinido, Ruta, HorarioRuta
from .serializers.rutas_historial_serializer import RutaSimpleSerializer, AsignacionRutaSerializer, HorarioAsignadoSerializer
from .serializers.horario_ruta_serializer import HorarioPredefinidoSerializer, HorarioRutaCreateSerializer, RutaSerializer, BusSerializer
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
# Create your views here.
class HorarioPredefinidoListView(ListAPIView):
    queryset = HorarioPredefinido.objects.all()
    serializer_class = HorarioPredefinidoSerializer
    
class RegistroConductorBusView(APIView):
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
    def get(self, request):
        desde_str = request.query_params.get('desde')
        hasta_str = request.query_params.get('hasta')

        desde = parse_date(desde_str) if desde_str else None
        hasta = parse_date(hasta_str) if hasta_str else None

        rutas = Ruta.objects.all()
        horarios = HorarioRuta.objects.all()

        if not desde and not hasta:
            hoy = date.today()
            rutas = rutas.filter(created_at__date=hoy)
            horarios = horarios.filter(created_at__date=hoy)
        else:
            if desde:
                rutas = rutas.filter(created_at__date__gte=desde)
                horarios = horarios.filter(created_at__date__gte=desde)
            if hasta:
                rutas = rutas.filter(created_at__date__lte=hasta)
                horarios = horarios.filter(created_at__date__lte=hasta)

        rutas_agregadas = rutas.order_by('-id')[:10]
        asignaciones = rutas.exclude(conductor__isnull=True).order_by('-id')[:10]
        horarios_asignados = horarios.order_by('-id')[:10]

        return Response({
            "rutas_agregadas": RutaSimpleSerializer(rutas_agregadas, many=True).data,
            "asignaciones_rutas": AsignacionRutaSerializer(asignaciones, many=True).data,
            "horarios_asignados": HorarioAsignadoSerializer(horarios_asignados, many=True).data
        })


class CrearRutaView(generics.CreateAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaCreateSerializer

class AsignarConductorRutaView(generics.UpdateAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaAsignarConductorSerializer
    lookup_field = 'numero_ruta'


class ListaConductoresView(generics.ListAPIView):
    queryset = Conductor.objects.all().order_by('nombre')
    serializer_class = ConductorListaSerializer

class CrearHorarioRutaView(generics.CreateAPIView):
    queryset = HorarioRuta.objects.all()
    serializer_class = HorarioRutaCreateSerializer
    
class DatosAsignacionRutaView(APIView):
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