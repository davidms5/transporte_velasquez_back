from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import User  # Importa el modelo original de Django


class CustomUserAdmin(UserAdmin):
    """Personaliza la vista de Django Admin para usuarios"""
    model = CustomUser

    # Campos que se mostrarán en el listado de usuarios
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    # Campos editables en la vista de edición/detalle de usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('role',)}),  # Agrega el campo "role" en la vista de detalle
    )

    # Campos editables en la vista de creación de usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('role',)}),  # Agrega el campo "role" en la creación
    )
    

admin.site.register(CustomUser, CustomUserAdmin)