"""
Configuración principal del proyecto core_project.

Los valores sensibles se leen desde variables de entorno con valores por
defecto válidos para desarrollo local. En producción (Render) la base de
datos se toma de `DATABASE_URL` (Neon PostgreSQL).
"""
import os
from pathlib import Path

import dj_database_url

# --------------------------------------------------------------------------- #
# Rutas
# --------------------------------------------------------------------------- #
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga opcional de variables de entorno desde un archivo .env local.
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except ImportError:  # pragma: no cover - dotenv es solo para desarrollo
    pass


def env_bool(name, default=False):
    """Convierte una variable de entorno en un valor booleano."""
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    """Convierte una variable de entorno separada por comas en una lista."""
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


# --------------------------------------------------------------------------- #
# Seguridad
# --------------------------------------------------------------------------- #
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "dev-insecure-secret-key-change-in-production"
)
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

# Orígenes de confianza para CSRF (dominios con esquema, ej. https://mi-app.onrender.com)
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

# --------------------------------------------------------------------------- #
# Aplicaciones
# --------------------------------------------------------------------------- #
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Aplicaciones del proyecto (modulares)
    "apps.users.apps.UsersConfig",
    "apps.inventory.apps.InventoryConfig",
    "apps.attendance.apps.AttendanceConfig",
    "apps.clients.apps.ClientsConfig",
    "apps.dashboard.apps.DashboardConfig",
    "apps.helpdesk.apps.HelpdeskConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise sirve los archivos estáticos en producción (Render).
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core_project.wsgi.application"
ASGI_APPLICATION = "core_project.asgi.application"

# --------------------------------------------------------------------------- #
# Base de datos
# --------------------------------------------------------------------------- #
# En producción se usa `DATABASE_URL` (Neon PostgreSQL). Si no existe, se
# recurre a las variables DB_* individuales (útil en desarrollo local).
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "core_project_db"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

# --------------------------------------------------------------------------- #
# Autenticación
# --------------------------------------------------------------------------- #
AUTH_USER_MODEL = "users.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "dashboard:index"
LOGOUT_REDIRECT_URL = "users:login"

# --------------------------------------------------------------------------- #
# Internacionalización
# --------------------------------------------------------------------------- #
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------- #
# Archivos estáticos y multimedia
# --------------------------------------------------------------------------- #
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise comprime y versiona los estáticos en producción.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------- #
# Seguridad en producción (Render termina el TLS y redirige a HTTPS)
# --------------------------------------------------------------------------- #
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS: se activa sólo si se define DJANGO_HSTS_SECONDS (>0) para evitar
    # bloquear dominios durante las pruebas iniciales.
    SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))
