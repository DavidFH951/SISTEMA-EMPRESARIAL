"""Vistas de la aplicación attendance."""
from datetime import time, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.users.mixins import role_required

from .models import AttendanceRecord

# Hora límite para considerar una entrada como tardanza.
LATE_THRESHOLD = time(9, 0)
# Hora estándar de salida.
STANDARD_CHECK_OUT = time(18, 0)


@login_required
def attendance_panel(request):
    """Vista del empleado para registrar su entrada/salida del día."""
    today = timezone.localdate()
    record = AttendanceRecord.objects.filter(user=request.user, date=today).first()
    recent_records = AttendanceRecord.objects.filter(user=request.user)[:10]
    context = {
        "today": today,
        "record": record,
        "recent_records": recent_records,
    }
    return render(request, "attendance/attendance_panel.html", context)


@login_required
@require_POST
def check_in(request):
    """Registra la hora de entrada del usuario autenticado."""
    today = timezone.localdate()
    now = timezone.localtime().time()

    record, _ = AttendanceRecord.objects.get_or_create(
        user=request.user, date=today
    )

    if record.check_in_time is not None:
        messages.warning(request, "Ya registraste tu entrada hoy.")
        return redirect("attendance:panel")

    record.check_in_time = now
    record.status = (
        AttendanceRecord.Status.LATE
        if now > LATE_THRESHOLD
        else AttendanceRecord.Status.PRESENT
    )
    record.save(update_fields=["check_in_time", "status"])
    messages.success(request, "Entrada registrada correctamente.")
    return redirect("attendance:panel")


@login_required
@require_POST
def check_out(request):
    """Registra la hora de salida del usuario autenticado."""
    today = timezone.localdate()
    now = timezone.localtime().time()

    record = AttendanceRecord.objects.filter(user=request.user, date=today).first()

    if record is None or record.check_in_time is None:
        messages.error(request, "Debes registrar tu entrada antes de la salida.")
        return redirect("attendance:panel")

    if record.check_out_time is not None:
        messages.warning(request, "Ya registraste tu salida hoy.")
        return redirect("attendance:panel")

    record.check_out_time = now
    record.save(update_fields=["check_out_time"])
    messages.success(request, "Salida registrada correctamente.")
    return redirect("attendance:panel")


@login_required
@role_required("ADMIN", "MANAGER")
def attendance_report(request):
    """Reporte de asistencia diario/semanal/mensual (Admin y Gerente)."""
    period = request.GET.get("period", "daily")
    today = timezone.localdate()

    if period == "weekly":
        start_date = today - timedelta(days=today.weekday())
    elif period == "monthly":
        start_date = today.replace(day=1)
    else:
        period = "daily"
        start_date = today

    records = (
        AttendanceRecord.objects.filter(date__gte=start_date, date__lte=today)
        .select_related("user")
    )

    context = {
        "period": period,
        "start_date": start_date,
        "end_date": today,
        "records": records,
        "summary": {
            "total": records.count(),
            "present": records.filter(
                status=AttendanceRecord.Status.PRESENT
            ).count(),
            "late": records.filter(status=AttendanceRecord.Status.LATE).count(),
            "absent": records.filter(status=AttendanceRecord.Status.ABSENT).count(),
            "leave": records.filter(status=AttendanceRecord.Status.LEAVE).count(),
        },
    }
    return render(request, "attendance/attendance_report.html", context)
