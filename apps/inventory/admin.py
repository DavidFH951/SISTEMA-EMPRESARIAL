"""Registro en el admin de la aplicación inventory."""
from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "stock_quantity", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("name", "sku", "description")
    ordering = ("-created_at",)
