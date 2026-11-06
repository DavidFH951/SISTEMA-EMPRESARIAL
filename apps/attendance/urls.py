"""Rutas de la aplicación attendance."""
from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_panel, name="panel"),
    path("entrada/", views.check_in, name="check_in"),
    path("salida/", views.check_out, name="check_out"),
    path("reporte/", views.attendance_report, name="report"),
]
