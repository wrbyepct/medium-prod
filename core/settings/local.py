# type: ignore
"""Local settings."""

# ruff: noqa: T201, ANN001, D103

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

ADMIN_URL = "supersecret/"  # new

# mailhog settings
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT", default=1025)
DEFAULT_FROM_EMAIL = "test@test.api.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Medium Clone"


# Django debug toolbar
if DEBUG and not IN_TEST:
    INSTALLED_APPS += ["debug_toolbar", "django_extensions"]  # += can also be used
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


def show_toolbar(request):
    client_ip: str = request.META.get("REMOTE_ADDR", "")
    print(f"client's ip is now: {client_ip}")
    return client_ip.startswith("172.") or client_ip == "127.0.0.1"


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}


# Elastic Search

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": [
            "http://es:9200",
        ]
    }
}
