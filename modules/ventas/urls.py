from django.urls import path
from .views import CrearTicketView, FacturasActivasView, AnularFacturaView, ReporteVentasView, CierreDiarioView, ResumenPorRutaView

urlpatterns = [
    path("tickets-crear/", CrearTicketView.as_view(), name="crear-ticket"),
    path("facturas-activas/", FacturasActivasView.as_view(), name="facturas-activas"),
    path("facturas/<str:numero_factura>/anular/", AnularFacturaView.as_view(), name="anular-factura"),
    path("reporte-dia/", ReporteVentasView.as_view(), name="reporte-ventas"),
    path('cierre-del-dia/', CierreDiarioView.as_view(), name='cierre-del-dia'),
    path("resumen-por-ruta/", ResumenPorRutaView.as_view(), name="resumen-por-ruta"),
]