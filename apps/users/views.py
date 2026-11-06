"""Vistas de autenticación de la aplicación users."""
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm


class CustomLoginView(LoginView):
    """Login con plantilla propia y redirección si el usuario ya está autenticado."""

    template_name = "users/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Cierre de sesión y regreso al login."""

    next_page = "users:login"
