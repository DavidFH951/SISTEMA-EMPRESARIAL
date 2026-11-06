"""Formularios de la aplicación helpdesk."""
from django import forms

from apps.users.models import CustomUser

from .models import Ticket, TicketAttachment, TicketComment


class TicketForm(forms.ModelForm):
    """Alta de tickets por parte de cualquier usuario autenticado."""

    class Meta:
        model = Ticket
        fields = ["title", "description", "category", "priority"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Resumen breve del problema o solicitud",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 6,
                    "placeholder": "Detalla el problema, pasos para reproducirlo, etc.",
                }
            ),
            "category": forms.Select(attrs={"class": "form-input"}),
            "priority": forms.Select(attrs={"class": "form-input"}),
        }


class TicketManageForm(forms.ModelForm):
    """Gestión de un ticket por parte del área de Sistemas."""

    class Meta:
        model = Ticket
        fields = ["status", "priority", "assigned_to"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-input"}),
            "priority": forms.Select(attrs={"class": "form-input"}),
            "assigned_to": forms.Select(attrs={"class": "form-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = CustomUser.objects.filter(
            department=CustomUser.Department.SYSTEMS
        )
        self.fields["assigned_to"].empty_label = "Sin asignar"
        self.fields["assigned_to"].required = False


class TicketCommentForm(forms.ModelForm):
    """Comentario de seguimiento sobre un ticket."""

    class Meta:
        model = TicketComment
        fields = ["body", "is_internal"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 3,
                    "placeholder": "Escribe un seguimiento...",
                }
            ),
            "is_internal": forms.CheckboxInput(
                attrs={"class": "form-check__input"}
            ),
        }


class TicketAttachmentForm(forms.ModelForm):
    """Carga de un archivo adjunto a un ticket."""

    class Meta:
        model = TicketAttachment
        fields = ["file"]
        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "form-input"}),
        }
