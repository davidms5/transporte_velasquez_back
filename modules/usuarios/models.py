from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

class CustomUser(AbstractUser):
    """Extiende el usuario de Django para incluir roles"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('operator', 'Operador'),
        ('supervisor', 'Supervisor'),
        ('billing', 'Facturación')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"