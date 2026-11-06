"""Modelos de la aplicación attendance."""
from django.conf import settings
from django.db import models


class AttendanceRecord(models.Model):
    """Registro diario de entrada/salida de un empleado."""

    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Presente"
        ABSENT = "ABSENT", "Ausente"
        LEAVE = "LEAVE", "Permiso"
        LATE = "LATE", "Tardanza"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        verbose_name="Usuario",
    )
    date = models.DateField("Fecha")
    check_in_time = models.TimeField("Hora de entrada", null=True, blank=True)
    check_out_time = models.TimeField("Hora de salida", null=True, blank=True)
    status = models.CharField(
        "Estado",
        max_length=10,
        choices=Status.choices,
        default=Status.ABSENT,
    )

    class Meta:
        verbose_name = "Registro de asistencia"
        verbose_name_plural = "Registros de asistencia"
        ordering = ["-date", "user__username"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="unique_attendance_per_user_per_day"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.get_status_display()})"

    @property
    def worked_hours(self):
        """Horas trabajadas en el día (si hay entrada y salida registradas)."""
        if not self.check_in_time or not self.check_out_time:
            return None
        start = self.check_in_time.hour * 60 + self.check_in_time.minute
        end = self.check_out_time.hour * 60 + self.check_out_time.minute
        if end < start:
            return None
        return round((end - start) / 60, 2)
