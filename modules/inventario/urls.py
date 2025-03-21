from django.urls import path
from .views import RegistrarRepuestoAPIView, RepuestosListView, HistorialRepuestosListView

urlpatterns = [
    path("registrar-repuesto/", RegistrarRepuestoAPIView.as_view(), name="registrar-repuesto"),
    path('get-repuestos/', RepuestosListView.as_view(), name='repuestos-list'),
    path('get-historial-repuestos/', HistorialRepuestosListView.as_view(), name='historial-list'),
]
