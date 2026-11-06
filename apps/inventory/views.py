"""Vistas para el panel de control (Dashboard)."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.clients.models import Cliente
from apps.helpdesk.models import Ticket
from apps.inventory.models import Activo  # ← Aquí está la corrección

class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista principal del panel de control."""
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas básicas
        context["total_clientes"] = Cliente.objects.count()
        context["tickets_abiertos"] = Ticket.objects.filter(estado="abierto").count()
        context["tickets_cerrados"] = Ticket.objects.filter(estado="cerrado").count()
        
        # Equipos disponibles (ajustado al nuevo modelo)
        context["equipos_disponibles"] = Activo.objects.filter(disponibilidad="DISPONIBLE").count()
        
        return context

class ProductListView(LoginRequiredMixin, ListView):
    """Listado de activos con búsqueda y filtro."""
    model = Activo
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        queryset = Activo.objects.all()

        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(
                Q(n_serie__icontains=search) | Q(codigo_interno__icontains=search)
            )

        stock_filter = self.request.GET.get("stock", "").strip()
        if stock_filter == "out":
            queryset = queryset.filter(disponibilidad="NO DISPONIBLE")
        elif stock_filter == "low":
            queryset = queryset.filter(disponibilidad="DISPONIBLE")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["stock_filter"] = self.request.GET.get("stock", "")
        return context


class ProductCreateView(RoleRequiredMixin, CreateView):
    """Alta de activos."""
    model = Activo
    fields = '__all__'  # Genera el formulario automático sin chocar con forms.py
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:product_list")
    allowed_roles = ("ADMIN", "MANAGER")


class ProductUpdateView(RoleRequiredMixin, UpdateView):
    """Edición de activos."""
    model = Activo
    fields = '__all__'
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:product_list")
    allowed_roles = ("ADMIN", "MANAGER")


class ProductDeleteView(RoleRequiredMixin, DeleteView):
    """Eliminación de activos."""
    model = Activo
    template_name = "inventory/product_confirm_delete.html"
    success_url = reverse_lazy("inventory:product_list")
    allowed_roles = ("ADMIN", "MANAGER")