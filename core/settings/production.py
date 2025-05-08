"""Production settings."""

from socket import gethostbyname, gethostname

ADMINS = [("Jay", "test@test.com")]
# TODO: add domain name for the production server
CSRF_TRUSTED_ORIGINS: list = []

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["l27.0.0.1"])


# Dynamically get the host address if we are running on ECS.
# We need this because ELB will make a request to health check
# So the request host is the internal ECS task IP address
if env("AWS_EXECUTION_ENV"):
    ALLOWED_HOSTS.append(gethostbyname(gethostname))

# Mail service
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_MAIL", default="test@test.api.com")


# AWS SES settings

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "email-smtp.ap-northeast-1.amazonaws.com"  # region must match SES
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # IAM user access key id
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # Converted IAM user secret accessky

DOMAIN = env("DOMAIN")
SITE_NAME = "Medium Clone"


# Elastic Search

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": [
            env("ELASTICSEARCH_URL"),
        ]
    }
}
