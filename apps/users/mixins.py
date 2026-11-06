"""Utilidades de control de acceso basadas en roles y áreas."""
from functools import wraps

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def user_has_role(user, allowed_roles):
    """Indica si el usuario pertenece a alguno de los roles permitidos."""
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    return user.role in allowed_roles


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin de vista basada en clases que exige sesión y rol permitido."""

    allowed_roles = ()

    def test_func(self):
        return user_has_role(self.request.user, self.allowed_roles)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("No tienes permisos para acceder a esta sección.")
        return super().handle_no_permission()


def role_required(*allowed_roles):
    """Decorador para vistas basadas en funciones que exige roles permitidos."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not user_has_role(request.user, allowed_roles):
                raise PermissionDenied(
                    "No tienes permisos para acceder a esta sección."
                )
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


def sistemas_required(view_func):
    """Restringe la vista al personal del área de Sistemas.

    Encapsula también la exigencia de sesión:
    - Usuario anónimo -> redirige al login conservando el `next`.
    - Usuario autenticado de otra área -> HTTP 403 (PermissionDenied).
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if not request.user.is_sistemas:
            raise PermissionDenied(
                "Esta sección es exclusiva del área de Sistemas."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped
