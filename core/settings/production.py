"""Production settings."""

ADMINS = [("Jay", "test@test.com")]
# TODO: add domain name for the production server
CSRF_TRUSTED_ORIGINS: list = []

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
