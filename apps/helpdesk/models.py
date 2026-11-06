"""Modelos de la aplicación helpdesk (Mesa de Ayuda interna)."""
from django.conf import settings
from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    """Ticket de soporte interno del sistema."""

    class Category(models.TextChoices):
        INCIDENT = "INCIDENT", "Incidente"
        SERVICE_REQUEST = "SERVICE_REQUEST", "Requerimiento de Servicio"
        ACCESS = "ACCESS", "Acceso/Permisos"
        HARDWARE = "HARDWARE", "Hardware"

    class Priority(models.TextChoices):
        LOW = "LOW", "Baja"
        MEDIUM = "MEDIUM", "Media"
        HIGH = "HIGH", "Alta"
        CRITICAL = "CRITICAL", "Crítica"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Abierto"
        IN_PROGRESS = "IN_PROGRESS", "En Proceso"
        ON_HOLD = "ON_HOLD", "En Espera"
        RESOLVED = "RESOLVED", "Resuelto"
        CLOSED = "CLOSED", "Cerrado"

    # Estados que marcan la resolución del ticket.
    RESOLVED_STATUSES = (Status.RESOLVED, Status.CLOSED)
    # Estados que siguen considerados como "abiertos" para métricas.
    ACTIVE_STATUSES = (Status.OPEN, Status.IN_PROGRESS, Status.ON_HOLD)

    ticket_id = models.CharField(
        "Código",
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False,
        help_text="Código correlativo con formato SYS-0001.",
    )
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción")
    category = models.CharField(
        "Categoría",
        max_length=20,
        choices=Category.choices,
        default=Category.INCIDENT,
    )
    priority = models.CharField(
        "Prioridad",
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        "Estado",
        max_length=15,
        choices=Status.choices,
        default=Status.OPEN,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
        verbose_name="Reportado por",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets",
        verbose_name="Asignado a",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado el", auto_now=True)
    resolved_at = models.DateTimeField("Resuelto el", null=True, blank=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
        ]

    def __str__(self):
        return f"{self.ticket_id or 'SYS-????'} - {self.title}"

    def save(self, *args, **kwargs):
        # Se persiste primero para obtener la clave primaria y derivar de
        # ella el código correlativo (evita condiciones de carrera).
        if self._state.adding and not self.ticket_id:
            super().save(*args, **kwargs)
            self.ticket_id = f"SYS-{self.pk:04d}"
            type(self).objects.filter(pk=self.pk).update(ticket_id=self.ticket_id)
            return

        # Sincroniza la marca de resolución con el estado.
        if self.status in self.RESOLVED_STATUSES:
            if self.resolved_at is None:
                self.resolved_at = timezone.now()
        else:
            self.resolved_at = None

        super().save(*args, **kwargs)

    @property
    def is_open(self):
        return self.status in self.ACTIVE_STATUSES

    @property
    def assignee_display(self):
        """Nombre legible del responsable asignado al ticket."""
        if self.assigned_to is None:
            return "Sin asignar"
        return self.assigned_to.get_full_name() or self.assigned_to.username


class TicketComment(models.Model):
    """Comentario o seguimiento asociado a un ticket."""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Ticket",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_comments",
        verbose_name="Autor",
    )
    body = models.TextField("Comentario")
    is_internal = models.BooleanField(
        "Nota interna",
        default=False,
        help_text="Las notas internas solo son visibles para el área de Sistemas.",
    )
    created_at = models.DateTimeField("Creado el", auto_now_add=True)

    class Meta:
        verbose_name = "Comentario de ticket"
        verbose_name_plural = "Comentarios de ticket"
        ordering = ["created_at"]

    def __str__(self):
        return f"Comentario de {self.author} en {self.ticket.ticket_id}"


class TicketAttachment(models.Model):
    """Archivo adjunto vinculado a un ticket."""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="Ticket",
    )
    file = models.FileField("Archivo", upload_to="helpdesk/attachments/%Y/%m/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_attachments",
        verbose_name="Subido por",
    )
    uploaded_at = models.DateTimeField("Subido el", auto_now_add=True)

    class Meta:
        verbose_name = "Adjunto de ticket"
        verbose_name_plural = "Adjuntos de ticket"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Adjunto de {self.ticket.ticket_id}: {self.file.name}"
