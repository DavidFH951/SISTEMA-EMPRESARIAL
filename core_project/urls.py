"""Rutas raíz del proyecto core_project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="dashboard:index", permanent=False)),
    path("", include("apps.users.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("inventario/", include("apps.inventory.urls")),
    path("asistencia/", include("apps.attendance.urls")),
    path("clientes/", include("apps.clients.urls")),
    path("helpdesk/", include("apps.helpdesk.urls")),
]

if settings.DEBUG:
    # Sirve los archivos adjuntos de la Mesa de Ayuda en desarrollo.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
