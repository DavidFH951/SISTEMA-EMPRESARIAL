"""Rutas de la aplicación inventory."""
from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("nuevo/", views.ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/editar/", views.ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/eliminar/", views.ProductDeleteView.as_view(), name="product_delete"),
]
