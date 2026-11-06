"""Modelos de la aplicación users."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Usuario del sistema con rol asignable por un administrador."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Gerente"
        EMPLOYEE = "EMPLOYEE", "Empleado"

    class Department(models.TextChoices):
        SYSTEMS = "Sistemas", "Sistemas"
        ACCOUNTING = "Contabilidad", "Contabilidad"
        HR = "Recursos Humanos", "Recursos Humanos"
        SALES = "Ventas", "Ventas"
        WAREHOUSE = "Almacén", "Almacén"
        OPERATIONS = "Operaciones", "Operaciones"
        OTHER = "Otros", "Otros"

    role = models.CharField(
        "Rol",
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        help_text="Define los permisos del usuario dentro del sistema.",
    )
    department = models.CharField(
        "Área",
        max_length=30,
        choices=Department.choices,
        default=Department.OTHER,
        help_text="Área a la que pertenece el usuario (ej. Sistemas).",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["username"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    @property
    def is_sistemas(self):
        """Indica si el usuario pertenece al área de Sistemas (Mesa de Ayuda)."""
        return self.department == self.Department.SYSTEMS or self.is_superuser
