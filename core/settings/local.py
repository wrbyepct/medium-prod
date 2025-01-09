# type: ignore
"""Local settings."""


# ruff: noqa: T201, ANN001, D103

SECRET_KEY = env("DJANGO_SECRET_KEY")

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

# mailhog settings
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "test@test.api.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Medium Clone"


# Django debug toolbar
INSTALLED_APPS += ["debug_toolbar"]  # += can also be used


def show_toolbar(request):
    client_ip: str = request.META.get("REMOTE_ADDR", "")
    print(f"client's ip is now: {client_ip}")
    return client_ip.startswith("172.") or client_ip == "127.0.0.1"


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
