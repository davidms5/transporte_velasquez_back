from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from typing import Final
# Create your models here.


class Constantes:
    
    ADMIN: Final = "admin"
    OPERATOR: Final = "operator"
    SUPERVISOR: Final = "supervisor"
    BILLING: Final = "billing"
    
    def __setattr__(self, name, value):
        raise TypeError("No puedes modificar una constante")
    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Constantes.ADMIN)  # Asigna el rol 'admin' por defecto
        return self.create_user(username, email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    """Extiende el usuario de Django para incluir roles"""  
    ROLE_CHOICES = [
        (Constantes.ADMIN, 'Admin'),
        (Constantes.OPERATOR, 'Operador'),
        (Constantes.SUPERVISOR, 'Supervisor'),
        (Constantes.BILLING, 'Facturación')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"