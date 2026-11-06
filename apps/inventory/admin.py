from django.contrib import admin
from .models import Ubicacion, Activo, Movimiento

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('id_ubicacion', 'tipo', 'nombre')

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('codigo_interno', 'tipo_equipo', 'marca', 'n_serie', 'estado', 'disponibilidad')
    search_fields = ('codigo_interno', 'n_serie')

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('activo', 'tipo_movimiento', 'desde', 'hacia', 'fecha', 'hora')
    list_filter = ('tipo_movimiento', 'fecha')
    