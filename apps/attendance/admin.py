"""Registro en el admin de la aplicación attendance."""
from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "check_in_time", "check_out_time", "status")
    list_filter = ("status", "date")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    date_hierarchy = "date"
    ordering = ("-date",)
