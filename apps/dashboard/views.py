from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.clients.models import Client
from apps.helpdesk.models import Ticket
from apps.inventory.models import Activo 
import traceback

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            context["total_clientes"] = Client.objects.count()
            context["tickets_abiertos"] = Ticket.objects.filter(estado="abierto").count()
            context["tickets_cerrados"] = Ticket.objects.filter(estado="cerrado").count()
            context["equipos_disponibles"] = Activo.objects.filter(disponibilidad="DISPONIBLE").count()
        except Exception as e:
            # Si algo falla, imprimimos el error exacto en la consola de Render
            print("========== ERROR EN EL DASHBOARD ==========")
            print(traceback.format_exc())
            print("===========================================")
        
        return context