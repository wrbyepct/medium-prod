# type: ignore
DEBUG = True

SECRET_KEY = env("DJANGO_SECRET_KEY")

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

ALLOWED_HOSTS = []
