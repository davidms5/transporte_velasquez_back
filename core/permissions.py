from rest_framework.permissions import BasePermission
from .Constantes import Constantes
class IsAdminOrReadOnly(BasePermission):
    """Permite acceso solo a administradores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
    
class IsAdminOrSupervisor(BasePermission):
    """
    Permite el acceso solo a usuarios con rol 'admin' o 'supervisor'
    """
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.role in [Constantes.ADMIN, Constantes.SUPERVISOR]


class IsAdminOrOperador(BasePermission):
    """
    Permite el acceso solo a usuarios con rol 'admin' o 'operador'
    """
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.role in [Constantes.ADMIN, Constantes.OPERATOR]
    
    
class IsAdminOrFacturacion(BasePermission):
    """
    Permite el acceso solo a usuarios con rol 'admin' o 'facturacion'
    """
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.role in [Constantes.ADMIN, Constantes.BILLING]