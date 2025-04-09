from django.urls import path
from .views import CrearTicketView, FacturasActivasView, AnularFacturaView, ReporteVentasView, CierreDiarioView

urlpatterns = [
    path("tickets-crear/", CrearTicketView.as_view(), name="crear-ticket"),
    path("facturas-activas/", FacturasActivasView.as_view(), name="facturas-activas"),
    path("facturas/<str:numero_factura>/anular/", AnularFacturaView.as_view(), name="anular-factura"),
    path("reporte-dia/", ReporteVentasView.as_view(), name="reporte-ventas"),
    path('ventas/cierre-del-dia/', CierreDiarioView.as_view(), name='cierre-del-dia'),
]