from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.http import JsonResponse
from django.middleware.csrf import get_token
from ..models import CustomUser, Constantes
from rest_framework.response import Response

def handle_login(request, access_token_str, base_response):
    
    try:
        decoded_token = AccessToken(access_token_str)
        username = decoded_token["username"]

        user = CustomUser.objects.get(username=username)
        refresh = RefreshToken.for_user(user)

        if user.is_staff or user.role == Constantes.ADMIN:
            
            login(request, user)
            
            request.session.save()
            #FIXME: ver tema de que no guarda y/o comparte el sessionid de la cookie,que necesito para loguearme en el admin
            # Enviar cookies de sesión y CSRF
            base_response.set_cookie(
                "sessionid",
                request.session.session_key,
                httponly=True,
                samesite="Lax"
            )
            base_response.set_cookie(
                "csrftoken",
                get_token(request),
                httponly=False,
                samesite="None"
            )
            base_response.data["redirect"] = "/admin/"

        #response = Response({'message': 'Login successful'}) TODO: cambiar esto despues para que el token no vaya en el body
        #FIXME: sessionid se guarda 2 veces
        base_response.set_cookie(
            key="jwt",
            value=str(refresh.access_token),
            httponly=False,  # Cambiar a True si no accedés desde JS
            secure=True,
            samesite="Lax"
        )

    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    except Exception as e:
        print(f"Error en login: {e}")

    return base_response

def handle_logout(request, refresh_token):
    
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": "Token inválido o ya expirado"}, status=400)
            
    logout(request)
    
    # 🧼 Limpiar cookies
    response = Response({"message": "Sesión cerrada correctamente"}, status=200)
    response.delete_cookie("jwt", samesite="Lax")
    response.delete_cookie("sessionid", samesite="Lax")
    response.delete_cookie("csrftoken", samesite="None")
    
    return response