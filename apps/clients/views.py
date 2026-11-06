"""Vistas de la aplicación clients."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    """Directorio de clientes con búsqueda por empresa o contacto."""

    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 20

    def get_queryset(self):
        queryset = Client.objects.all()
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(
                Q(company_name__icontains=search)
                | Q(contact_name__icontains=search)
                | Q(email__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context
