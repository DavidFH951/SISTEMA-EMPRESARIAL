"""Rutas de la aplicación helpdesk."""
from django.urls import path

from . import views

app_name = "helpdesk"

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("nuevo/", views.ticket_create, name="ticket_create"),
    path("panel/", views.helpdesk_dashboard, name="dashboard"),
    path("<str:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path("<str:ticket_id>/gestionar/", views.ticket_manage, name="ticket_manage"),
    path(
        "<str:ticket_id>/comentar/",
        views.ticket_comment_create,
        name="comment_create",
    ),
    path(
        "<str:ticket_id>/adjuntar/",
        views.ticket_attachment_create,
        name="attachment_create",
    ),
]
