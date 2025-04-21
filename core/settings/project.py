# type: ignore
"""Settings specific for this project."""

from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # This is for authentication for view access.
    "DEFAULT_AUTHENTICATION_CLASSES": ["dj_rest_auth.jwt_auth.JWTCookieAuthentication"],
    # Meaning all views are not 'public' by default.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.BrowsableAPIRenderer",  # This enables the UI
        "rest_framework.renderers.JSONRenderer",
    ],
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": env("JWT_SIGNING_KEY"),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# dj-rest-auth
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "medium-access-token",
    "JWT_AUTH_REFRESH_COOKIE": "medium-refresh-token",
    "REGISTER_SERIALIZER": "core.apps.user.serializers.CustomRegisterSerializer",
}

# allauth
AUTHENTICATION_BACKENDS = {
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = None

# Doc
SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "TITLE": "Medium API",
    "DESCRIPTION": "A Medium Clone API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # License information
    "LICENSE": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    # Contact information
    "CONTACT": {
        "name": "API Support Team",
        "email": "support@testapi.com",
        "url": "https://testapi.com/contact",
    },
}

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": [
            "http://es:9200",
        ]
    }
}

# AWS SES settings
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"  # AWS SES backend name
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT", default=1025)
DEFAULT_FROM_EMAIL = "test@test.api.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Medium Clone"


EMAIL_HOST_USER = "YOUR_SMTP_USERNAME"  # IAM user access key id
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # Converted IAM user secret accessky
