from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """Permite acceso solo a administradores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
