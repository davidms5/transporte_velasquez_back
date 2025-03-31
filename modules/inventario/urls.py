from django.urls import path
from .views import RegistrarRepuestoAPIView, RepuestosListView, HistorialRepuestosListView, RepuestoDetailCustomView, FacturaListCreateView, FacturaRetrieveUpdateView, FacturaSoftDeleteView


urlpatterns = [
    path("registrar-repuesto/", RegistrarRepuestoAPIView.as_view(), name="registrar-repuesto"),
    path('get-repuestos/', RepuestosListView.as_view(), name='repuestos-list'),
    path('get-historial-repuestos/', HistorialRepuestosListView.as_view(), name='historial-list'),
    path('get-repuesto/<int:id>/', RepuestoDetailCustomView.as_view(), name='repuesto-detail'), #TODO: capaz eso se puede mejorar a futuro para recibir params en su lugar
    
    #facturas
    path('facturas/', FacturaListCreateView.as_view(), name='factura-list-create'),
    path('facturas/<str:codigo>/', FacturaRetrieveUpdateView.as_view(), name='factura-detail-update'),
    path('facturas/<str:codigo>/delete/', FacturaSoftDeleteView.as_view(), name='factura-soft-delete'),
]
