"""Modelos de la aplicación clients."""
from django.db import models


class Client(models.Model):
    """Cliente corporativo registrado en el sistema."""

    company_name = models.CharField("Empresa", max_length=150)
    contact_name = models.CharField("Persona de contacto", max_length=150)
    email = models.EmailField("Correo electrónico")
    phone = models.CharField("Teléfono", max_length=30, blank=True)
    address = models.CharField("Dirección", max_length=255, blank=True)
    registered_at = models.DateTimeField("Registrado el", auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["company_name"]

    def __str__(self):
        return self.company_name
