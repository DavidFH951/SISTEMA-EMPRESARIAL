"""Rutas de la aplicación dashboard."""
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_index, name="index"),
]
