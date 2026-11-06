"""Formularios de la aplicación users."""
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Formulario de login con clases CSS aplicadas a los widgets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-input",
                "placeholder": "Nombre de usuario",
                "autocomplete": "username",
                "autofocus": True,
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-input",
                "placeholder": "Contraseña",
                "autocomplete": "current-password",
            }
        )
