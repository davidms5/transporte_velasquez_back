from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth import login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from django.middleware.csrf import get_token
from .models import CustomUser, Constantes
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .service.auth_service import handle_login, handle_logout
# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def login_admin(request):
    
    user = request.user
    if user.role != "admin" or user.is_staff:
        return JsonResponse({"error": "No autorizado"}, status=403)
    
    login(request, user)
    return JsonResponse({"message": "Bienvenido!"})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Si el login fue exitoso, obtener el token de acceso
        if response.status_code == 200:
            access_token = response.data.get("access")
            return handle_login(request, access_token, response)

        return response

class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # 🔓 Invalidar refresh token si se envió
        refresh_token = request.data.get("refresh")
        return handle_logout(request, refresh_token)