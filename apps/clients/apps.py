"""Configuración de la aplicación clients."""
from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clients"
    verbose_name = "Clientes"
