# type: ignore
"""Local settings."""

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
