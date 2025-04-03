from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth import login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from django.middleware.csrf import get_token
from .models import CustomUser, Constantes
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
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

            try:
                print("aqui: ",access_token)
                decoded_token = AccessToken(access_token)
                username = decoded_token["username"]

                # Autenticar al usuario en Django
                user = CustomUser.objects.get(username=username)
                refresh = RefreshToken.for_user(user)
                
                if user.is_staff or user.role == Constantes.ADMIN:
                    
                    login(request, user)  # Crear sesión en Django Admin

                    request.session.save()
                    #FIXME: ver tema de que no guarda y/o comparte el sessionid de la cookie,que necesito para loguearme en el admin
                    # Enviar cookies de sesión y CSRF
                    response.set_cookie("sessionid", request.session.session_key, httponly=True, samesite="Lax")
                    response.set_cookie("csrftoken", get_token(request), httponly=False, samesite="None")

                    # Redirigir automáticamente al panel de administración si es admin
                    response.data["redirect"] = "/admin/" #TODO: poner esto en un env
                    
                    #response = Response({'message': 'Login successful'}) TODO: cambiar esto despues para que el token no vaya en el body
                    #FIXME: sessionid se guarda 2 veces
                response.set_cookie(
                    key='jwt',
                    value=str(refresh.access_token),
                    httponly=False,  # Cambiar a True si no necesitas acceder al token desde JavaScript TODO:
                    #secure=True,  # Solo si estás en HTTPS
                    samesite='Lax'
                )
            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "Usuario no encontrado"}, status=404)
            except Exception as e:
                print(f"Error al autenticar en Django Admin: {e}")

        return response
