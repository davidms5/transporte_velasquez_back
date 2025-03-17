from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from typing import Final
# Create your models here.


class Constantes:
    
    ADMIN: Final = "admin"
    OPERATOR: Final = "operator"
    SUPERVISOR: Final = "supervisor"
    BILLING: Final = "billing"
    
    def __setattr__(self, name, value):
        raise TypeError("No puedes modificar una constante")
    
    
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