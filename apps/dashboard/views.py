from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.clients.models import Cliente
from apps.helpdesk.models import Ticket
from apps.inventory.models import Activo 

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["total_clientes"] = Cliente.objects.count()
        context["tickets_abiertos"] = Ticket.objects.filter(estado="abierto").count()
        context["tickets_cerrados"] = Ticket.objects.filter(estado="cerrado").count()
        context["equipos_disponibles"] = Activo.objects.filter(disponibilidad="DISPONIBLE").count()
        
        return context