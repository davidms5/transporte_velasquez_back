from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """Usa el serializer personalizado para incluir el rol en el JWT"""
    serializer_class = CustomTokenObtainPairSerializer

# Create your views here.
