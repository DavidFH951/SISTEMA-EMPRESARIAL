"""Vistas de la aplicación helpdesk (Mesa de Ayuda interna)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.users.mixins import sistemas_required

from .forms import (
    TicketAttachmentForm,
    TicketCommentForm,
    TicketForm,
    TicketManageForm,
)
from .models import Ticket, TicketAttachment, TicketComment


def _can_view(user, ticket):
    """Un usuario de Sistemas ve todo; el resto solo sus propios tickets."""
    return user.is_sistemas or ticket.created_by_id == user.pk


@login_required
def ticket_list(request):
    """Listado de tickets.

    El área de Sistemas ve todos los tickets con filtros; el resto de usuarios
    solo visualiza los tickets que han reportado.
    """
    tickets = Ticket.objects.select_related("created_by", "assigned_to")

    if not request.user.is_sistemas:
        tickets = tickets.filter(created_by=request.user)
    else:
        category = request.GET.get("category", "").strip()
        status_filter = request.GET.get("status", "").strip()
        priority = request.GET.get("priority", "").strip()

        if category:
            tickets = tickets.filter(category=category)
        if status_filter:
            tickets = tickets.filter(status=status_filter)
        if priority:
            tickets = tickets.filter(priority=priority)

    search = request.GET.get("q", "").strip()
    if search:
        tickets = tickets.filter(
            Q(ticket_id__icontains=search) | Q(title__icontains=search)
        )

    context = {
        "tickets": tickets,
        "search_query": search,
        "category_filter": request.GET.get("category", ""),
        "status_filter": request.GET.get("status", ""),
        "priority_filter": request.GET.get("priority", ""),
        "categories": Ticket.Category.choices,
        "statuses": Ticket.Status.choices,
        "priorities": Ticket.Priority.choices,
        "can_manage": request.user.is_sistemas,
    }
    return render(request, "helpdesk/ticket_list.html", context)


@login_required
def ticket_create(request):
    """Alta de un ticket por parte del usuario solicitante."""
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(
                request, f"Ticket {ticket.ticket_id} registrado correctamente."
            )
            return redirect("helpdesk:ticket_detail", ticket_id=ticket.ticket_id)
    else:
        form = TicketForm()

    return render(request, "helpdesk/ticket_form.html", {"form": form})


@login_required
def ticket_detail(request, ticket_id):
    """Detalle del ticket con su historial de seguimiento."""
    ticket = get_object_or_404(
        Ticket.objects.select_related("created_by", "assigned_to"),
        ticket_id=ticket_id,
    )
    if not _can_view(request.user, ticket):
        raise PermissionDenied("Solo puedes ver los tickets que has reportado.")

    comments = ticket.comments.select_related("author")
    if not request.user.is_sistemas:
        comments = comments.filter(is_internal=False)

    context = {
        "ticket": ticket,
        "comments": comments,
        "attachments": ticket.attachments.select_related("uploaded_by"),
        "comment_form": TicketCommentForm(),
        "attachment_form": TicketAttachmentForm(),
        "can_manage": request.user.is_sistemas,
    }
    return render(request, "helpdesk/ticket_detail.html", context)


@login_required
@require_POST
def ticket_comment_create(request, ticket_id):
    """Agrega un comentario de seguimiento al ticket."""
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if not _can_view(request.user, ticket):
        raise PermissionDenied("No puedes comentar en este ticket.")

    form = TicketCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.ticket = ticket
        comment.author = request.user
        # Las notas internas solo las puede crear el área de Sistemas.
        if not request.user.is_sistemas:
            comment.is_internal = False
        comment.save()
        messages.success(request, "Comentario agregado.")
    else:
        messages.error(request, "El comentario no puede estar vacío.")

    return redirect("helpdesk:ticket_detail", ticket_id=ticket.ticket_id)


@login_required
@require_POST
def ticket_attachment_create(request, ticket_id):
    """Adjunta un archivo al ticket."""
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if not _can_view(request.user, ticket):
        raise PermissionDenied("No puedes adjuntar archivos a este ticket.")

    form = TicketAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        attachment = form.save(commit=False)
        attachment.ticket = ticket
        attachment.uploaded_by = request.user
        attachment.save()
        messages.success(request, "Archivo adjuntado correctamente.")
    else:
        messages.error(request, "Selecciona un archivo válido.")

    return redirect("helpdesk:ticket_detail", ticket_id=ticket.ticket_id)


@sistemas_required
def ticket_manage(request, ticket_id):
    """Gestión del ticket (estado, prioridad y asignación). Solo Sistemas."""
    ticket = get_object_or_404(
        Ticket.objects.select_related("created_by"), ticket_id=ticket_id
    )

    if request.method == "POST":
        form = TicketManageForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket actualizado correctamente.")
            return redirect("helpdesk:ticket_detail", ticket_id=ticket.ticket_id)
    else:
        form = TicketManageForm(instance=ticket)

    return render(
        request, "helpdesk/ticket_manage.html", {"ticket": ticket, "form": form}
    )


@sistemas_required
def helpdesk_dashboard(request):
    """Panel de soporte con métricas de la Mesa de Ayuda. Solo Sistemas."""
    tickets = Ticket.objects.select_related("created_by", "assigned_to")
    active = tickets.exclude(status__in=Ticket.RESOLVED_STATUSES)

    context = {
        "total": tickets.count(),
        "open_count": tickets.filter(status=Ticket.Status.OPEN).count(),
        "in_progress_count": tickets.filter(
            status=Ticket.Status.IN_PROGRESS
        ).count(),
        "unassigned_count": active.filter(assigned_to__isnull=True).count(),
        "critical_count": active.filter(priority=Ticket.Priority.CRITICAL).count(),
        "recent_tickets": active[:10],
        "by_category": [
            {
                "label": label,
                "count": tickets.filter(category=value).count(),
            }
            for value, label in Ticket.Category.choices
        ],
    }
    return render(request, "helpdesk/dashboard.html", context)
