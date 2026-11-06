"""Vistas de la aplicación dashboard."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from apps.attendance.models import AttendanceRecord
from apps.clients.models import Client
from apps.inventory.models import Product
from apps.users.models import CustomUser


@login_required
def dashboard_index(request):
    """Vista resumen con los indicadores principales del sistema."""
    today = timezone.localdate()

    context = {
        "total_users": CustomUser.objects.count(),
        "products_in_stock": Product.objects.filter(stock_quantity__gt=0).count(),
        "total_clients": Client.objects.count(),
        "today_attendance": AttendanceRecord.objects.filter(date=today).count(),
        "today": today,
    }
    return render(request, "dashboard/index.html", context)
