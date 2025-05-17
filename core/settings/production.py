"""Production settings."""

# ruff: noqa: ERA001
from socket import gethostbyname, gethostname

import boto3
from elasticsearch import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

ADMINS = [("Jay", "seaweednick3738@gmail.com")]
CSRF_TRUSTED_ORIGINS: list = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["l27.0.0.1"])


# Dynamically get the host address if we are running on ECS.
# We need this because ELB will make a request to health check
# So the request host is the internal ECS task IP address
if env("AWS_EXECUTION_ENV"):
    ALLOWED_HOSTS.append(gethostbyname(gethostname()))

ALB_HOST = env("ALB_HOST")
if ALB_HOST:
    ALLOWED_HOSTS.append(ALB_HOST)

# AWS SES settings

DOMAIN = env("DOMAIN")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

EMAIL_FAIL_SILENTLY = False  # TODO: Set to true when in full prod mode

EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = f"noreply@{DOMAIN}"


SITE_NAME = "Medium Clone"


# AWS OpenSearch
session = boto3.Session()
credentials = session.get_credentials()
region = env("AWS_DEFAULT_REGION")
aws_auth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    "es",
    session_token=credentials.token,
)

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": f"{env('ELASTICSEARCH_URL')}:443",
        "http_auth": aws_auth,
        "use_ssl": True,
        "verify_certs": True,
        "connection_class": RequestsHttpConnection,
    }
}

# Admin URL
ADMIN_URL = env("DJANGO_ADMIN_URL")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",  # or DEBUG for full tracebacks
            "propagate": False,
        },
    },
}

DEBUG = True  # TODO: Set to true when in full prod mode
