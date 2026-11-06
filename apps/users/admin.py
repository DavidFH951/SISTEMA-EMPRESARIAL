"""Registro en el admin de la aplicación users."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Permite a los administradores crear usuarios y asignar roles."""

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "department",
        "is_active",
    )
    list_filter = ("role", "department", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Roles del sistema", {"fields": ("role", "department")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Roles del sistema", {"fields": ("role", "department")}),
    )
