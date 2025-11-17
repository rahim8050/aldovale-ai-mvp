import os
from pathlib import Path
from typing import Any
import dj_database_url
import pymysql
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

pymysql.install_as_MySQLdb()
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
# --- Environment ---
DJANGO_ENV = os.getenv("DJANGO_ENV", "development")
IS_PROD = DJANGO_ENV == "production"
IS_TEST = bool(os.environ.get("PYTEST_CURRENT_TEST"))

SECRET_KEY = os.getenv("SECRET_KEY") or get_random_secret_key()
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
ALLOWED_HOSTS: list[str] = [
    "localhost",
    "127.0.0.1",
    "aldovale-ai-mvp.onrender.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "apps.core",
    "apps.chat",
    "aldovale_ai",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "aldovale.urls"

TEMPLATES: list[dict[str, Any]] = [
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

WSGI_APPLICATION = "aldovale.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# --- Database ---
DATABASES = {
    "default": dj_database_url.config(
        # fallback for local dev if DATABASE_URL not set
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=IS_PROD,
    )
}

# --- MySQL specific tuning ---
if DATABASES["default"].get("ENGINE") == "django.db.backends.mysql":
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"].update(
        {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES', time_zone='+00:00'",
            "charset": "utf8mb4",
            "use_unicode": True,
        }
    )
    DATABASES["default"]["CONN_HEALTH_CHECKS"] = True

# --- Pytest: in-memory SQLite ---
if IS_TEST:
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    }


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.core.authentication.ClientJWTAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "core.renderes.GlobalResponseRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Aldovale AI API",
    "DESCRIPTION": "Backend API documentation for Aldovale AI — secure, scalable, and production-ready.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_AUTHENTICATION": [],  # disable for public docs if desired
    "SERVE_PERMISSIONS": [],  # adjust for internal access
}

STATIC_URL = "/static/"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")
    return value


if os.environ.get("DJANGO_ENV") == "production":
    EXPECTED_API_KEY = require_env("EXPECTED_API_KEY")
    JWT_SECRET_KEY = require_env("JWT_SECRET_KEY")
else:
    EXPECTED_API_KEY = os.environ.get("EXPECTED_API_KEY", "test-api-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "test-jwt-secret")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
