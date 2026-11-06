"""Registro en el admin de la aplicación clients."""
from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_name", "email", "phone", "registered_at")
    search_fields = ("company_name", "contact_name", "email")
    ordering = ("company_name",)
