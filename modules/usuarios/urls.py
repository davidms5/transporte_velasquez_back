from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Para obtener el token
    TokenRefreshView,  # Para refrescar el token
    TokenVerifyView  # Para verificar si un token es válido
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), TODO: ver como manejar esto mejor despues de cara a la seguridad
    path('verify/', TokenVerifyView.as_view(), name='token_verify'), #post
]
