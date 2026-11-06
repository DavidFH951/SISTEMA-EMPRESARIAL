"""Registro en el admin de la aplicación helpdesk."""
from django.contrib import admin

from .models import Ticket, TicketAttachment, TicketComment


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    readonly_fields = ("created_at",)


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0
    readonly_fields = ("uploaded_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_id",
        "title",
        "category",
        "priority",
        "status",
        "created_by",
        "assigned_to",
        "created_at",
    )
    list_filter = ("status", "priority", "category", "created_at")
    search_fields = ("ticket_id", "title", "description", "created_by__username")
    readonly_fields = ("ticket_id", "created_at", "updated_at", "resolved_at")
    date_hierarchy = "created_at"
    inlines = (TicketCommentInline, TicketAttachmentInline)
    ordering = ("-created_at",)


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "is_internal", "created_at")
    list_filter = ("is_internal", "created_at")
    search_fields = ("ticket__ticket_id", "author__username", "body")


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "file", "uploaded_by", "uploaded_at")
    search_fields = ("ticket__ticket_id", "uploaded_by__username")
