"""Vistas de la aplicación inventory."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.users.mixins import RoleRequiredMixin

from .forms import ProductForm
from .models import Product


class ProductListView(LoginRequiredMixin, ListView):
    """Listado de productos con búsqueda y filtro por nivel de stock."""

    model = Product
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.all()

        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(sku__icontains=search)
            )

        stock_filter = self.request.GET.get("stock", "").strip()
        if stock_filter == "low":
            queryset = queryset.filter(stock_quantity__lte=5)
        elif stock_filter == "out":
            queryset = queryset.filter(stock_quantity=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["stock_filter"] = self.request.GET.get("stock", "")
        return context


class ProductCreateView(RoleRequiredMixin, CreateView):
    """Alta de productos (solo Admin y Gerente)."""

    model = Product
    form_class = ProductForm
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:product_list")
    allowed_roles = ("ADMIN", "MANAGER")


class ProductUpdateView(RoleRequiredMixin, UpdateView):
    """Edición de productos (solo Admin y Gerente)."""

    model = Product
    form_class = ProductForm
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("inventory:product_list")
    allowed_roles = ("ADMIN", "MANAGER")


class ProductDeleteView(RoleRequiredMixin, DeleteView):
    """Eliminación de productos (solo Admin y Gerente)."""

    model = Product
    template_name = "inventory/product_confirm_delete.html"
    success_url = reverse_lazy("inventory:product_list")
    allowed_roles = ("ADMIN", "MANAGER")
