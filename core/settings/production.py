"""Production settings."""

# ruff: noqa: ERA001
from socket import gethostbyname, gethostname

ADMINS = [("Jay", "test@test.com")]
# TODO: add domain name for the production server
CSRF_TRUSTED_ORIGINS: list = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["l27.0.0.1"])


# Dynamically get the host address if we are running on ECS.
# We need this because ELB will make a request to health check
# So the request host is the internal ECS task IP address
if env("AWS_EXECUTION_ENV"):
    ALLOWED_HOSTS.append(gethostbyname(gethostname()))

# Mail service
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_MAIL", default="test@test.api.com")


# AWS SES settings

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "email-smtp.ap-northeast-1.amazonaws.com"  # region must match SES
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # IAM user access key id
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # Converted IAM user secret accessky

DOMAIN = env("DOMAIN")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

EMAIL_FAIL_SILENTLY = False

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = f"noreply@{DOMAIN}.com"


SITE_NAME = "Medium Clone"


# Elastic Search

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": [
            env("ELASTICSEARCH_URL"),
        ]
    }
}

# Admin URL
ADMIN_URL = env("DJANGO_ADMIN_URL")
