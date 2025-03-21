from django.urls import path
from .views import RegistrarRepuestoAPIView

urlpatterns = [
    path("registrar-repuesto/", RegistrarRepuestoAPIView.as_view(), name="registrar-repuesto")
]
