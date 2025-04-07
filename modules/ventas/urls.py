from django.urls import path
from .views import CrearTicketView

urlpatterns = [
    path("tickets/crear/", CrearTicketView.as_view(), name="crear-ticket"),
]