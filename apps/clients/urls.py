"""Rutas de la aplicación clients."""
from django.urls import path

from . import views

app_name = "clients"

urlpatterns = [
    path("", views.ClientListView.as_view(), name="client_list"),
]
