"""Production settings."""

# ruff: noqa: ERA001
from socket import gethostbyname, gethostname

import boto3
from opensearchpy import (
    AWSV4SignerAuth,
    RequestsHttpConnection,
)

ADMINS = [("Jay", "seaweednick3738@gmail.com")]
CSRF_TRUSTED_ORIGINS: list = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1"])


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

EMAIL_BACKEND = "django_ses.SESBackend"
AWS_SES_REGION_NAME = env("AWS_DEFAULT_REGION")
DEFAULT_FROM_EMAIL = f"noreply@{DOMAIN}"


SITE_NAME = "Medium Clone"


# AWS OpenSearch
session = boto3.Session()
credentials = session.get_credentials()
region = env("AWS_DEFAULT_REGION")

OPENSEARCH_DSL = {
    "default": {
        # Use your OpenSearch domain host and port:
        "hosts": [
            {
                "host": env(
                    "ELASTICSEARCH_URL"
                ),  # e.g. "my-domainID.us-west-2.es.amazonaws.com"
                "port": 443,
            }
        ],
        # Provide AWS SigV4 auth with IAM credentials
        "http_auth": AWSV4SignerAuth(credentials, region, service="es"),
        "use_ssl": True,  # Use https
        "verify_certs": True,  # verify domain cert on OpenSearch
        "connection_class": RequestsHttpConnection,  # allow es to use http request
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
