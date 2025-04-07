from django.urls import path
from .views import (
    HorarioPredefinidoListView, 
    RegistroConductorBusView, 
    HistorialRutasView, 
    CrearRutaView, 
    AsignarConductorRutaView, 
    ListaConductoresView,
    CrearHorarioRutaView,
    DatosAsignacionRutaView,
    RutasSinHorarioView,
    RutasConHorarioView,
    HorariosDeRutaView)
    


# urls.py
urlpatterns = [
    path('registro/conductor-bus/', RegistroConductorBusView.as_view(), name='registro-conductor-bus'),
    path('horarios/predefinidos/', HorarioPredefinidoListView.as_view(), name='horarios-predefinidos'),
    path('historial/rutas/', HistorialRutasView.as_view(), name='historial-rutas'),
    path('rutas/crear/', CrearRutaView.as_view(), name='crear-ruta'),
    path('rutas/<int:numero_ruta>/asignar-conductor/', AsignarConductorRutaView.as_view(), name='asignar-conductor'),
    path('rutas/datos-asignacion/', DatosAsignacionRutaView.as_view(), name='datos-asignacion-ruta'),
    path('conductores/', ListaConductoresView.as_view(), name='lista-conductores'),
    path('horarios/asignar/', CrearHorarioRutaView.as_view(), name='crear-horario-ruta'),
    path('horarios/rutas-disponibles/', RutasSinHorarioView.as_view(), name='rutas-disponibles'),
    path("rutas-con-horario/", RutasConHorarioView.as_view(), name="rutas-con-horario"),
    path("rutas/<str:numero_ruta>/horarios/", HorariosDeRutaView.as_view(), name="horarios-ruta")

]

