"""
URL configuration for inventario_buses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import MEDIA_URL, MEDIA_ROOT, DEBUG
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core.permissions import IsAdminOrReadOnly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Esquema JSON de OpenAPI
    
    #rutas de la api
    path("api/usuarios/", include("modules.usuarios.urls"))
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT) #TODO: revisar despues ^media/(?P<path>.*)$

if DEBUG:  # Solo habilitar Swagger en modo desarrollo TODO: ver como manejar mejor esto despues
    urlpatterns += [
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # UI de Swagger
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # UI de ReDoc
    ]