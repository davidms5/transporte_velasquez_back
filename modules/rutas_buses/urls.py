from django.urls import path
from .views import (
    HorarioPredefinidoListView, 
    RegistroConductorBusView, 
    HistorialRutasView, 
    CrearRutaView, 
    AsignarConductorRutaView, 
    ListaConductoresView,
    CrearHorarioRutaView)
    


# urls.py
urlpatterns = [
    path('registro/conductor-bus/', RegistroConductorBusView.as_view(), name='registro-conductor-bus'),
    path('horarios/predefinidos/', HorarioPredefinidoListView.as_view(), name='horarios-predefinidos'),
    path('historial/rutas/', HistorialRutasView.as_view(), name='historial-rutas'),
    path('rutas/crear/', CrearRutaView.as_view(), name='crear-ruta'),
    path('rutas/<int:id>/asignar-conductor/', AsignarConductorRutaView.as_view(), name='asignar-conductor'),
    path('conductores/', ListaConductoresView.as_view(), name='lista-conductores'),
    path('horarios/asignar/', CrearHorarioRutaView.as_view(), name='crear-horario-ruta'),
]

