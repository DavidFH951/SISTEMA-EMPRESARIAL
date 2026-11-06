"""Modelos de la aplicación inventory."""
from django.db import models


class Product(models.Model):
    """Producto almacenado en el inventario."""

    name = models.CharField("Nombre", max_length=150)
    sku = models.CharField("SKU", max_length=50, unique=True)
    description = models.TextField("Descripción", blank=True)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField("Cantidad en stock", default=0)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado el", auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def is_low_stock(self):
        """Marca productos con existencias por debajo del umbral mínimo."""
        return self.stock_quantity <= 5
